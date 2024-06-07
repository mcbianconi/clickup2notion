from .base_adapter import ClickUpToNotionAdapter


class DatesAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        creation_date = clickup_data.get("date_created", "")
        update_date = clickup_data.get("date_updated", "")
        due_date = clickup_data.get("due_date", "")

        notion_dates = {}
        if creation_date:
            notion_dates["Creation Date"] = {"date": {"start": creation_date}}
        if update_date:
            notion_dates["Update Date"] = {"date": {"start": update_date}}
        if due_date:
            notion_dates["Due Date"] = {"date": {"start": due_date}}
        return {"properties": notion_dates}
