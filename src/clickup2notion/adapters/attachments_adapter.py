from typing import Any
from .base_adapter import ClickUpToNotionAdapter


class AttachmentsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        attachments = clickup_data.get("Attachments", [])
        children = []
        
        if attachments:
            children.append({
            "object": "block",
            "type": "divider",
            "divider": {},
            })
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Anexos"},
                        },
                    ]
                },
            })
            for attachment in attachments:
                children.append(
                    {
                        "object": "block",
                        "type": "external",
                        "external": {"url": attachment["url"]},
                    }
                )
        
        return {"children": children}
