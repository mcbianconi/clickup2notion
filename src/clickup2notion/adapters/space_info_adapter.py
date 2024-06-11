from .base_adapter import ClickUpToNotionAdapter


class SpaceInfoAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        return {
            "properties": {
                "Space": {"select": {"name": clickup_data.get("Space Name")}},
                "Folder": {"select": {"name": clickup_data.get("Folder Name")}},
                "List": {"select": {"name": clickup_data.get("List Name")}},
                "Task Custom ID": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": clickup_data.get("Task Custom ID", "")},
                        }
                    ],
                },
            }
        }
