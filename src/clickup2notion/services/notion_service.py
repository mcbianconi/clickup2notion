import asyncio
import logging

logger = logging.getLogger("notion_service")

async def create_database_properties(notion_client, database_id):
    database = await notion_client.databases.retrieve(database_id=database_id)
    existing_properties = database.get("properties", {})

    new_properties = {
        "ClickUp URL": {"url": {}},
        "Clickup Created time": {"date": {}},
        "Clickup Last edited time": {"date": {}},
        "Due date": {"date": {}},
        "Tags": {"multi_select": {}},
        "Status": {"select": {}},
        "Space": {"select": {}},
        "Folder": {"select": {}},
        "List": {"select": {}},
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
        await notion_client.databases.update(database_id=database_id, **update_data)


async def create_page(notion_client, page_data):
    semaphore = asyncio.Semaphore(3)
    try:
        async with semaphore:
            await notion_client.pages.create(**page_data)
            logger.info(f"Página criada no Notion: {page_data}")
            await asyncio.sleep(1)  # isso + semáforo = 3 requests per second = rate limit da API deles
    except Exception as err:
        logger.exception(f"Erro ao criar página no Notion: {err}")
