from abc import ABC, abstractmethod


class ClickUpToNotionAdapter(ABC):
    @abstractmethod
    def convert(self, clickup_data: dict) -> dict:
        pass
