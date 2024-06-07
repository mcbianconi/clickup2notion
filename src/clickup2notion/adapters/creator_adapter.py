from .base_adapter import ClickUpToNotionAdapter


class CreatorAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        creator = clickup_data.get("creator", {}).get("email", "???")
        return {
            "children": {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": creator,
                            },
                        }
                    ]
                },
            }
        }
