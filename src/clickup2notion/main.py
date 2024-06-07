import os
import click
import asyncio
from clickup2notion.services.migration_service import export
from dotenv import load_dotenv

load_dotenv()


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
