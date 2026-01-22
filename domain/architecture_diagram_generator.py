from config import MERMAID_GRAPH_TYPE, CORE_NODE_LABEL, MERMAID_MISSING_ARCHITECTURE_MSG
from domain.diagram_generator import MermaidDiagramGenerator
from domain.node_id_generator import NodeIdGenerator


class ArchitectureDiagramGenerator(MermaidDiagramGenerator):
    def __init__(self, node_id_generator: NodeIdGenerator):
        self._node_id_generator = node_id_generator

    def generate(self, service_data: dict) -> str:
        interfaces = service_data.get("interfaces", {})

        if not interfaces:
            return f"{MERMAID_GRAPH_TYPE}\n    MissingArchitecture[{MERMAID_MISSING_ARCHITECTURE_MSG}]"

        # Extract service information
        service = service_data.get("service", {})
        service_id = service.get("id", "")
        service_name = service.get("name", "")
        service_version = service.get("version", "")
        runtime = service.get("runtime", {})
        runtime_language = runtime.get("language", "")
        runtime_version = runtime.get("version", "")
        capabilities = service.get("capabilities", [])

        # Build Core label with service information
        core_label_parts = [CORE_NODE_LABEL]
        if service_id:
            core_label_parts.append(f"ID: {service_id}")
        if service_name:
            core_label_parts.append(f"{service_name}")
        if service_version:
            core_label_parts.append(f"V{service_version}")
        if runtime_language and runtime_version:
            core_label_parts.append(f"{runtime_language} {runtime_version}")

        core_label = "<br/>".join(core_label_parts)

        lines = [
            MERMAID_GRAPH_TYPE,
            f'    Core["{core_label}"]',
        ]

        for interface_name, interface_config in interfaces.items():
            port_type = interface_config.get("port")
            if not port_type:
                continue

            technology = interface_config.get("technology", "")
            enabled = interface_config.get("enabled", True)
            enabled_icon = "✓" if enabled else "✗"

            interface_id = self._node_id_generator.generate(interface_name)

            # Build label with technology
            label_parts = [f"{enabled_icon} {interface_name}"]
            if technology:
                label_parts.append(f"({technology})")

            # Add base_path or location if present
            base_path = interface_config.get("base_path")
            location = interface_config.get("location")
            exchanges = interface_config.get("exchanges")
            if base_path:
                label_parts.append(base_path)
            elif location:
                label_parts.append(location)
            elif exchanges:
                exchange_names = [ex.get("name") for ex in exchanges if ex.get("name")]
                if exchange_names:
                    label_parts.append(", ".join(exchange_names))

            label = "<br/>".join(label_parts)
            lines.append(f'    {interface_id}["{label}"]')

            if port_type == "input":
                lines.append(f"    {interface_id} --> Core")
            elif port_type == "output":
                lines.append(f"    Core --> {interface_id}")

        return "\n".join(lines)
