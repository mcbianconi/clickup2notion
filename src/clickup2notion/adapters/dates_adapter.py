import logging
from clickup2notion.utils.helpers import timestamp_to_ISO8601

from .base_adapter import ClickUpToNotionAdapter

logger = logging.getLogger("adapter")


class DatesAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        creation_date_text = clickup_data.get("Date Created", "")
        try:
            creation_date = timestamp_to_ISO8601(creation_date_text)
        except Exception:
            logger.error(
                f"Erro de parse Date Created: {creation_date_text} - task ID {clickup_data.get('Task ID')} ({clickup_data.get('Task Custom ID')})"
            )
            creation_date = None

        return {
            "properties": {
                "Clickup Created time": {"date": {"start": creation_date}},
            }
        }
