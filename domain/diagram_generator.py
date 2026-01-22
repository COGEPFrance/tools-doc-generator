from abc import ABC, abstractmethod


class MermaidDiagramGenerator(ABC):
    @abstractmethod
    def generate(self, service_data: dict) -> str: ...
