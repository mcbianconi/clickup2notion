import asyncio
import logging

from notion_client import AsyncClient
from clickup2notion.adapters.attachments_adapter import AttachmentsAdapter
from clickup2notion.adapters.comments_adapter import CommentsAdapter
from clickup2notion.adapters.composite_adapter import CompositeAdapter
from clickup2notion.adapters.due_date_adapter import DatesAdapter
from clickup2notion.adapters.subtasks_adapter import SubtasksAdapter
from clickup2notion.adapters.tags_adapter import TagsAdapter
from clickup2notion.adapters.task_name_adapter import TaskNameAdapter
from clickup2notion.services import clickup_service
from clickup2notion.services import notion_service

logger = logging.getLogger("migration_service")

composite_adapter = CompositeAdapter()
composite_adapter.add(TaskNameAdapter())
composite_adapter.add(DatesAdapter())
composite_adapter.add(SubtasksAdapter())
composite_adapter.add(TagsAdapter())
composite_adapter.add(AttachmentsAdapter())
composite_adapter.add(CommentsAdapter())


async def create_notion_page(notion, task, notion_database_id):
    notion_task = clickup2notion(task, notion_database_id)
    try:
        await notion.pages.create(**notion_task)
    except Exception as err:
        logger.error(f"Erro ao criar página no Notion: {err}")


def clickup2notion(clickup_task, parent_page_id):

    notion_data = composite_adapter.convert(clickup_task)

    notion_data.update({"parent": {"database_id": parent_page_id}})

    notion_service.create_notion_properties(notion, parent_page_id)
    return notion_data


async def export(
    clickup_list_id, notion_database_id, clickup_api_token, notion_api_token
):
    notion = AsyncClient(auth=notion_api_token)

    await notion_service.create_notion_properties(notion, notion_database_id)

    async with clickup_service.get_session(clickup_api_token) as clickup_session:

        tasks = await clickup_service.get_clickup_tasks(
            clickup_session, clickup_list_id
        )

        get_attachment_tasks = []
        create_page_tasks = []

        for task in tasks:
            get_attachment_tasks.append(
                clickup_service.get_task_attachments(clickup_session, task)
            )

            notion_task = clickup2notion(task)
            create_page_tasks.append(
                create_notion_page(notion, notion_task, notion_database_id)
            )

        await asyncio.gather(*get_attachment_tasks)

        logger.info(f"Criando {len(create_page_tasks)} páginas no Notion")
        await asyncio.gather(*create_page_tasks)
