from .base_adapter import ClickUpToNotionAdapter


class SpaceInfoAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        return {
            "properties": {
                "Space": {"select": {"name": clickup_data.get("Space Name")}},
                "Folder": {"select": {"name": clickup_data.get("Folder Name")}},
                "List": {"select": {"name": clickup_data.get("List Name")}},
            }
        }
