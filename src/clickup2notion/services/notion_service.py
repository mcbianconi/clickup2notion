import logging

logger = logging.getLogger("notion_service")


async def create_notion_properties(notion_client, database_id):
    database = await notion_client.databases.retrieve(database_id=database_id)
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
        await notion_client.databases.update(database_id=database_id, **update_data)
