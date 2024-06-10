import asyncio
import logging

from clickup2notion.adapters.composite_adapter import CompositeAdapter

from clickup2notion.services import clickup_service, notion_service

from notion_client import AsyncClient


logger = logging.getLogger("migration_service")


async def export(clickup_csv_path, notion_database_id, notion_api_token):
    all_tasks = clickup_service.parse_csv_tasks(clickup_csv_path)

    notion_client = AsyncClient(auth=notion_api_token)
    await notion_service.create_database_properties(notion_client, notion_database_id),

    notion_adapter = CompositeAdapter(notion_database_id)

    async with asyncio.TaskGroup() as g:
        for clickup_task in all_tasks:
            page_data = notion_adapter.convert(clickup_task)
            g.create_task(notion_service.create_page(notion_client, page_data))
        logger.info("Starting migration")

    logger.info("Migration completed")
