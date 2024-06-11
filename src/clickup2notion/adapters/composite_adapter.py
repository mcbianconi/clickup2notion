from typing import cast
import logging

from .tags_adapter import TagsAdapter
from .attachments_adapter import AttachmentsAdapter
from .comments_adapter import CommentsAdapter
from .dates_adapter import DatesAdapter
from .description_adapter import DescriptionAdapter
from .space_info_adapter import SpaceInfoAdapter
from .status_adapter import StatusAdapter
from .task_name_adapter import TaskNameAdapter
from .base_adapter import ClickUpToNotionAdapter


class CompositeAdapter(ClickUpToNotionAdapter):
    def __init__(self, parent_page_id: str):
        self._parent_page_id = parent_page_id
        self._logger = logging.getLogger("NotionDBRowAdapter")
        self._children = [
            TaskNameAdapter(),
            DescriptionAdapter(),
            StatusAdapter(),
            DatesAdapter(),
            AttachmentsAdapter(),
            CommentsAdapter(),
            SpaceInfoAdapter(),
            TagsAdapter(),
        ]

    def add(self, adapter: ClickUpToNotionAdapter):
        self._children.append(adapter)

    def convert(self, clickup_data: dict) -> dict:
        self._logger.debug(f"Converting ClickUp data to Notion data: {clickup_data}")
        notion_data: dict = {"properties": {}, "children": []}
        for child in self._children:
            child_data = child.convert(clickup_data)
            notion_data = cast(
                dict, self._merge_dicts(cast(dict, notion_data), child_data)
            )
        notion_data.update({"parent": {"database_id": self._parent_page_id}})
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
