from .base_adapter import ClickUpToNotionAdapter


class ClickupURLAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        url = clickup_data["url"]
        return {"properties": {"ClickUp URL": {"url": url}}}
