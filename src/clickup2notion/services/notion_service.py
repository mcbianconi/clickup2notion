import asyncio
import logging

logger = logging.getLogger("notion_service")


async def create_database_properties(notion_client, database_id):
    database = await notion_client.databases.retrieve(database_id=database_id)
    existing_properties = database.get("properties", {})

    new_properties = {
        "Clickup Created time": {"date": {}},
        "Tags": {"multi_select": {}},
        "Status": {"select": {}},
        "Space": {"select": {}},
        "Folder": {"select": {}},
        "List": {"select": {}},
        "Task Custom ID": {"rich_text": {}},
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


_create_page_semaphore = asyncio.Semaphore(3)


async def create_page(notion_client, page_data):
    try:
        async with _create_page_semaphore:
            await notion_client.pages.create(**page_data)
            logger.info(f"Página criada no Notion: {page_data}")
            await asyncio.sleep(
                1
            )  # isso + semáforo de 3 requests per second = dentro do rate limit da API deles
    except Exception as err:
        logger.exception(f"Erro ao criar página no Notion: {err}\n")
