from .base_adapter import ClickUpToNotionAdapter
from clickup2notion.utils.helpers import split_text


class DescriptionAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        description = clickup_data.get("Task Content", "???")
        description_chunks = description.replace("\\n", "\n").split("\n")
        children = []
        for chunk in description_chunks:
            children.append(
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
            )

        return {"children": children}
