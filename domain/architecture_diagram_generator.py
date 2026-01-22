from config import MERMAID_GRAPH_TYPE, CORE_NODE_LABEL, MERMAID_MISSING_ARCHITECTURE_MSG
from domain.diagram_generator import MermaidDiagramGenerator
from domain.node_id_generator import NodeIdGenerator


class ArchitectureDiagramGenerator(MermaidDiagramGenerator):
    def __init__(self, node_id_generator: NodeIdGenerator):
        self._node_id_generator = node_id_generator

    def generate(self, service_data: dict) -> str:
        ports = service_data.get("architecture", {}).get("ports")

        if not ports:
            return f"{MERMAID_GRAPH_TYPE}\n    MissingArchitecture[{MERMAID_MISSING_ARCHITECTURE_MSG}]"

        lines = [
            MERMAID_GRAPH_TYPE,
            f'    Core["{CORE_NODE_LABEL}"]',
        ]

        for port_name, direction in ports.items():
            port_id = self._node_id_generator.generate(port_name)
            lines.append(f'    {port_id}["{port_name}"]')

            if direction == "input":
                lines.append(f"    {port_id} --> Core")
            elif direction == "output":
                lines.append(f"    Core --> {port_id}")

        return "\n".join(lines)
