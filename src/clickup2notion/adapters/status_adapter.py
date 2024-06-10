from .base_adapter import ClickUpToNotionAdapter


class StatusAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        status = clickup_data["Status"]
        return {"properties": {"Status": {"select": {"name": status}}}}
