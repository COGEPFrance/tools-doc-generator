from pathlib import Path


class FileSystemDiagramWriter:
    def write(self, output_dir: Path, filename: str, content: str) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / filename).write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Generated {output_dir / filename}")
