from .base_adapter import ClickUpToNotionAdapter


class TagsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        tags = clickup_data.get("Tags", [])
        notion_tags = []
        for tag in tags:
            if tag:
                notion_tags.append({"name": tag})
        return {"properties": {"Tags": {"multi_select": notion_tags}}}
