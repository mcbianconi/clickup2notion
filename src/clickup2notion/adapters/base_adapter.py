from abc import ABC, abstractmethod
from typing import Any, TypedDict


class ClickUpToNotionAdapter(ABC):
    @abstractmethod
    def convert(self, clickup_data: dict) -> dict:
        pass
