from .base_adapter import ClickUpToNotionAdapter
from clickup2notion.utils.helpers import split_text


class DescriptionAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        description = clickup_data.get("Task Content", "???")
        return {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": chunk,
                                },
                            }
                        ]
                    },
                }
                for chunk in split_text(description)
            ]
        }
