from .base_adapter import ClickUpToNotionAdapter


class SubtasksAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        subtasks = clickup_data.get("subtasks", [])
        return {
            "children": [
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {"type": "text", "text": {"content": subtask["name"]}}
                        ],
                        "checked": subtask.get("checked", False),
                    },
                }
                for subtask in subtasks
            ]
        }
