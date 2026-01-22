#!/usr/bin/env python3

import sys
from pathlib import Path

from adapters.yaml_loader import YAMLServiceDataLoader
from adapters.filesystem_writer import FileSystemDiagramWriter
from domain.node_id_generator import NodeIdGenerator
from domain.architecture_diagram_generator import ArchitectureDiagramGenerator
from domain.messaging_diagram_generator import MessagingDiagramGenerator
from application.orchestrator import DiagramGenerationOrchestrator, DiagramConfig


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_mermaid.py <service.yaml> <output_dir>")
        sys.exit(1)

    service_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    node_id_generator = NodeIdGenerator()
    loader = YAMLServiceDataLoader()
    writer = FileSystemDiagramWriter()

    diagram_configs = [
        DiagramConfig("architecture.mmd", ArchitectureDiagramGenerator(node_id_generator)),
        DiagramConfig("messaging.mmd", MessagingDiagramGenerator(node_id_generator)),
    ]

    orchestrator = DiagramGenerationOrchestrator(loader, writer, diagram_configs)
    orchestrator.generate_all(service_file, output_dir)


if __name__ == "__main__":
    main()
