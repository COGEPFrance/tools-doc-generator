import yaml
from pathlib import Path


class YAMLServiceDataLoader:
    def load(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
