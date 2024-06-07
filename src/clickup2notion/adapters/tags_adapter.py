from .base_adapter import ClickUpToNotionAdapter


class TagsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        tags = clickup_data.get("tags", [])
        notion_tags = [{"name": tag.get("name")} for tag in tags]
        return {"properties": {"Tags": {"multi_select": notion_tags}}}
