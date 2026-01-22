from config import MERMAID_GRAPH_TYPE, SERVICE_NODE_LABEL, MERMAID_NO_RABBITMQ_MSG
from domain.diagram_generator import MermaidDiagramGenerator
from domain.node_id_generator import NodeIdGenerator


class MessagingDiagramGenerator(MermaidDiagramGenerator):
    def __init__(self, node_id_generator: NodeIdGenerator):
        self._node_id_generator = node_id_generator

    def generate(self, service_data: dict) -> str:
        rabbit = service_data.get("interfaces", {}).get("rabbitmq")

        if not rabbit or not rabbit.get("enabled"):
            return f"{MERMAID_GRAPH_TYPE}\n    NoRabbitMQ[{MERMAID_NO_RABBITMQ_MSG}]"

        lines = [
            MERMAID_GRAPH_TYPE,
            f'    MS["{SERVICE_NODE_LABEL}"]',
        ]

        exchanges = self._build_exchanges(rabbit, lines)
        queues = self._build_queues(rabbit, lines)
        self._add_consumes(rabbit, queues, lines)
        self._add_publishes(rabbit, exchanges, lines)

        return "\n".join(lines)

    def _build_exchanges(self, rabbit: dict, lines: list[str]) -> dict[str, str]:
        exchanges = {}
        for ex in rabbit.get("exchanges", []):
            name = ex["name"]
            eid = self._node_id_generator.generate(name)
            exchanges[name] = eid
            lines.append(f'    {eid}["{name}<br/>({ex["type"]})"]')
        return exchanges

    def _build_queues(self, rabbit: dict, lines: list[str]) -> dict[str, str]:
        queues = {}
        for q in rabbit.get("queues", []):
            name = q["name"]
            qid = self._node_id_generator.generate(name)
            queues[name] = qid
            lines.append(f'    {qid}([{name}])')
        return queues

    def _add_consumes(self, rabbit: dict, queues: dict[str, str], lines: list[str]) -> None:
        for c in rabbit.get("consumes", {}).get("commands", []):
            q = c["queue"]
            if q in queues:
                lines.append(f"    {queues[q]} --> MS")

    def _add_publishes(self, rabbit: dict, exchanges: dict[str, str], lines: list[str]) -> None:
        for e in rabbit.get("publishes", {}).get("events", []):
            ex = e["exchange"]
            if ex in exchanges:
                lines.append(f"    MS --> {exchanges[ex]}")
