from config import MERMAID_GRAPH_TYPE, MERMAID_NO_RABBITMQ_MSG
from domain.diagram_generator import MermaidDiagramGenerator
from domain.node_id_generator import NodeIdGenerator


class MessagingDiagramGenerator(MermaidDiagramGenerator):
    def __init__(self, node_id_generator: NodeIdGenerator):
        self._node_id_generator = node_id_generator

    def generate(self, service_data: dict) -> str:
        interfaces = service_data.get("interfaces", {})

        message = interfaces.get("message", {})

        if not message.get("enabled"):
            return f"{MERMAID_GRAPH_TYPE}\n    NoRabbitMQ[{MERMAID_NO_RABBITMQ_MSG}]"

        lines = [MERMAID_GRAPH_TYPE]

        exchanges = {}
        queues = {}

        # Exchanges
        for ex in message.get("exchanges", []):
            name = ex["name"]
            eid = self._node_id_generator.generate(name)
            exchanges[name] = eid
            lines.append(f'    {eid}["{name}<br/>({ex["type"]})"]')

        # Queues with routing_key and supports for commands
        commands_consumes = message.get("consumes", {}).get("commands", [])

        for q in message.get("queues", []):
            name = q["name"]
            qid = self._node_id_generator.generate(name)

            # Check if this is a commands queue to add routing_key and supports
            queue_label_parts = [name]
            for c in commands_consumes:
                if c["queue"] == name:
                    routing_key = c.get("routing_key")
                    supports = c.get("supports", [])
                    if routing_key:
                        queue_label_parts.append(f"routing: {routing_key}")
                    if supports:
                        queue_label_parts.append(f"{'<br /> - '.join(supports)}")
                    break

            queue_label = "<br/> - ".join(queue_label_parts)
            queues[name] = qid
            lines.append(f'    {qid}([{queue_label}])')

        # Consumes: commands.queue -> exchange
        for c in commands_consumes:
            q = c["queue"]
            if q in queues and exchanges:
                first_exchange = list(exchanges.values())[0]
                lines.append(f"    {queues[q]} --> {first_exchange}")

        # Find dlq and events.queue
        dlq_id = None
        events_queue_id = None

        for queue_name, queue_id in queues.items():
            if "dlq" in queue_name.lower():
                dlq_id = queue_id
            elif "events" in queue_name.lower():
                events_queue_id = queue_id

        # Connect exchange to events.queue and dlq
        if exchanges:
            first_exchange = list(exchanges.values())[0]
            if events_queue_id:
                lines.append(f"    {first_exchange} --> {events_queue_id}")
            if dlq_id:
                lines.append(f"    {first_exchange} --> {dlq_id}")

        # Create event nodes as children of events.queue
        events_publishes = message.get("publishes", {}).get("events", [])

        if events_queue_id:
            for event in events_publishes:
                event_name = event.get("name")
                if event_name:
                    event_id = self._node_id_generator.generate(event_name)
                    lines.append(f'    {event_id}["{event_name}"]')
                    lines.append(f"    {events_queue_id} --> {event_id}")

        return "\n".join(lines)

