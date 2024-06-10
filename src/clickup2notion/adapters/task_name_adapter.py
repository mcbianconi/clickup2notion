from .base_adapter import ClickUpToNotionAdapter


class TaskNameAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        return {
            "properties": {
                "Nome": {
                    "title": [{"text": {"content": clickup_data.get("Task Name", "")}}]
                }
            }
        }
