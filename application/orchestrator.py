from dataclasses import dataclass
from pathlib import Path

from ports import ServiceDataLoader, DiagramWriter
from domain.diagram_generator import MermaidDiagramGenerator


@dataclass(frozen=True)
class DiagramConfig:
    filename: str
    generator: MermaidDiagramGenerator


class DiagramGenerationOrchestrator:
    def __init__(
        self,
        loader: ServiceDataLoader,
        writer: DiagramWriter,
        diagram_configs: list[DiagramConfig],
    ):
        self._loader = loader
        self._writer = writer
        self._diagram_configs = diagram_configs

    def generate_all(self, service_file: Path, output_dir: Path) -> None:
        service_data = self._loader.load(service_file)

        for config in self._diagram_configs:
            content = config.generator.generate(service_data)
            self._writer.write(output_dir, config.filename, content)
