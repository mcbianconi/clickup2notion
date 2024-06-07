from .base_adapter import ClickUpToNotionAdapter


class AttachmentsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        attachments = clickup_data.get("attachments", [])
        notion_attachments = [
            {
                "object": "block",
                "type": "file",
                "file": {
                    "external": {"url": attachment["url"]},
                    "name": attachment["title"],
                },
            }
            for attachment in attachments
            if not attachment.get("deleted")
        ]
        return {"children": notion_attachments}
