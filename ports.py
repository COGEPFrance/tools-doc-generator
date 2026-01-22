from typing import Protocol
from pathlib import Path


class ServiceDataLoader(Protocol):
    def load(self, path: Path) -> dict: ...


class DiagramWriter(Protocol):
    def write(self, output_dir: Path, filename: str, content: str) -> None: ...
