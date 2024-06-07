from .base_adapter import ClickUpToNotionAdapter

_priority_translation = {
    "urgent": "Alta",
    "high": "Alta",
    "normal": "Normal",
    "Medium": "Normal",
    "low": "Baixa",
}


class PriorityAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        url = clickup_data["url"]
        return {
            "properties": {
                "Prioridade": {
                    "select": {"name": _determine_notion_priority(clickup_data)}
                }
            }
        }


def _determine_notion_priority(clickup_data):
    priority = "Medium"
    priority_data = clickup_data.get("priority")
    if priority_data:
        priority = priority_data.get("priority")
    try:
        return _priority_translation[priority]
    except KeyError:
        return "???"
