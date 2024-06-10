import os
import click

from aiohttp_client_cache import CachedSession
from aiohttp_client_cache.backends.filesystem import FileBackend
import asyncio
import logging

from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("clickup2notion")

attachment_semaphore = asyncio.Semaphore(value=3)

_attachments_store = {}


async def get_task_attachments(session, task):
    url = f"https://api.clickup.com/api/v2/task/{task['id']}"
    async with attachment_semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            clickup_task_data = await response.json()
            attachments = clickup_task_data["attachments"]
            if len(attachments) > 0:
                _attachments_store[task["id"]] = attachments
            logger.info(
                f"Encontrados {len(clickup_task_data['attachments'])} anexos na tarefa {task['id']}"
            )
            await asyncio.sleep(1)


async def get_clickup_tasks(clickup_session, list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task?include_markdown_description=true"
    query = {
        "page": "0",
        "archived": "false",
        "include_markdown_description": "true",
    }

    tasks = []

    while True:
        async with clickup_session.get(url, params=query) as response:
            response.raise_for_status()
            list_data = await response.json()
            tasks.extend(list_data["tasks"])
            if list_data["last_page"]:
                break
            query["page"] = str(int(query["page"]) + 1)

    logger.info(f"Encontradas {len(tasks)} tarefas no ClickUp")
    return tasks


async def create_notion_properties(notion_database_id, notion):
    database = await notion.databases.retrieve(database_id=notion_database_id)
    existing_properties = database.get("properties", {})

    new_properties = {
        "ClickUp URL": {"url": {}},
        "Prioridade": {
            "select": {
                "options": [
                    {"name": "high", "color": "red"},
                    {"name": "normal", "color": "yellow"},
                    {"name": "low", "color": "green"},
                ]
            }
        },
    }

    properties_to_update = {
        key: value
        for key, value in new_properties.items()
        if key not in existing_properties
    }

    if properties_to_update:
        logger.info(f"Atualizando {len(properties_to_update)} propriedades no Notion")
        update_data = {"properties": properties_to_update}
        await notion.databases.update(database_id=notion_database_id, **update_data)


def split_text(text, max_length=2000) -> list[str]:
    if not text:
        return [""]
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]


async def create_notion_page(notion: AsyncClient, task, notion_database_id) -> None:
    content = []
    content_chunks = split_text(task["text_content"])
    for chunk in content_chunks:
        content.append({"text": {"content": chunk}})

    page_data = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "Nome": {"title": [{"text": {"content": task["name"]}}]},
            "Prioridade": {"select": {"name": task["priority"]}},
            "ClickUp URL": {"url": task["clickup_url"]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Autor: {task['creator']}",
                            },
                        }
                    ]
                },
            },
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": task["text_content"],
                            },
                        }
                    ]
                },
            },
        ],
    }

    if task["id"] in _attachments_store:

        attachments = [
            {
                "object": "block",
                "type": "file",
                "file": {
                    "external": {"url": attachment["url"]},
                    "name": attachment["title"],
                },
            }
            for attachment in _attachments_store[task["id"]]
            if not attachment["deleted"]
        ]

        page_data["children"].extend(attachments)

    try:
        await notion.pages.create(**page_data)
    except Exception as err:
        logger.error(f"Erro ao criar página no Notion: {err}")


async def export(
    clickup_list_id, notion_database_id, clickup_api_token, notion_api_token
):
    notion = AsyncClient(auth=notion_api_token)
    await create_notion_properties(notion_database_id, notion)

    clickup_headers = {"Authorization": clickup_api_token}

    file_cache = FileBackend(cache_name="clickup", allowable_codes=(200, 404))

    async with CachedSession(
        headers=clickup_headers, cache=file_cache
    ) as clickup_session:

        tasks = await get_clickup_tasks(clickup_session, clickup_list_id)

        get_attachment_tasks = []
        create_page_tasks = []

        for task in tasks:
            get_attachment_tasks.append(
                get_task_attachments(clickup_session, task, attachment_semaphore)
            )

            notion_task = clickup2notion(task)
            create_page_tasks.append(
                create_notion_page(notion, notion_task, notion_database_id)
            )

        logger.info(
            f"Pegando anexos de {len(get_attachment_tasks)} tarefas com {attachment_semaphore._value} requisições simultâneas"
        )
        await asyncio.gather(*get_attachment_tasks)

        logger.info(f"Criando {len(create_page_tasks)} páginas no Notion")
        await asyncio.gather(*create_page_tasks)


def clickup2notion(clickup_task):
    notion_task = {
        "id": clickup_task["id"],
        "name": clickup_task["name"],
        "text_content": clickup_task.get("description", ""),
        "priority": determine_notion_priority(clickup_task),
        "clickup_url": clickup_task["url"],
        "tags": clickup_task["tags"],
        "creator": clickup_task["creator"]["email"],
        "status": clickup_task["status"]["type"],
    }

    return notion_task


def determine_notion_priority(clickup_task):
    _priority_translation = {
        "urgent": "Alta",
        "high": "Alta",
        "normal": "Normal",
        "Medium": "Normal",
        "low": "Baixa",
    }
    priority = "Medium"
    priority_data = clickup_task.get("priority")
    if priority_data:
        priority = priority_data.get("priority")
    try:
        return _priority_translation[priority]
    except KeyError:
        return "???"


@click.command()
@click.option("--clickup_list_id", required=True, help="ID da lista do ClickUp")
@click.option(
    "--notion_database_id", required=True, help="ID da base de dados do Notion"
)
def main(clickup_list_id, notion_database_id):
    clickup_api_token = os.getenv("CLICKUP_API_TOKEN")
    notion_api_token = os.getenv("NOTION_API_TOKEN")

    if not clickup_api_token or not notion_api_token:
        click.echo(
            "Os tokens de API não foram encontrados. Verifique seu arquivo .env."
        )
        return

    asyncio.run(
        export(clickup_list_id, notion_database_id, clickup_api_token, notion_api_token)
    )


if __name__ == "__main__":
    main()
