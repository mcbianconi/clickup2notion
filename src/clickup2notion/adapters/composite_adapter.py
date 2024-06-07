from .base_adapter import ClickUpToNotionAdapter


class CompositeAdapter(ClickUpToNotionAdapter):
    def __init__(self):
        self._children = []

    def add(self, adapter: ClickUpToNotionAdapter):
        self._children.append(adapter)

    def convert(self, clickup_data: dict) -> dict:
        notion_data: dict = {"properties": {}, "children": []}
        for child in self._children:
            child_data = child.convert(clickup_data)
            notion_data = self._merge_dicts(notion_data, child_data)
        return notion_data

    def _merge_dicts(self, dict1: dict, dict2: dict) -> dict:
        for key in dict2:
            if (
                key in dict1
                and isinstance(dict1[key], list)
                and isinstance(dict2[key], list)
            ):
                dict1[key].extend(dict2[key])
            elif (
                key in dict1
                and isinstance(dict1[key], dict)
                and isinstance(dict2[key], dict)
            ):
                dict1[key] = self._merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        return dict1
