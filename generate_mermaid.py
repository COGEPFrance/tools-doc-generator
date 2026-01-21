#!/usr/bin/env python3

import sys
import yaml
from pathlib import Path


# --------------------------------------------------
# Utils
# --------------------------------------------------

def load_service(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_diagram(output_dir: Path, filename: str, content: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Generated {output_dir / filename}")


def node_id(value: str) -> str:
    return value.replace(".", "_").replace("-", "_")


# --------------------------------------------------
# Diagram 1 — Service / Interfaces
# --------------------------------------------------

def generate_service_diagram(svc: dict) -> str:
    service = svc["service"]
    interfaces = svc.get("interfaces", {})

    lines = [
        "graph TB",
        f'    MS["{service["name"]}<br/>v{service["version"]}"]',
    ]

    # API
    api = interfaces.get("api")
    if api and api.get("enabled"):
        label = f'HTTP API<br/>{api["base_path"]}'
        lines.append(f'    API["{label}"]')
        lines.append("    API --> MS")

    # CLI
    cli = interfaces.get("cli")
    if cli and cli.get("enabled"):
        lines.append('    CLI["CLI"]')
        lines.append("    CLI --> MS")

    # RabbitMQ
    rabbit = interfaces.get("rabbitmq")
    if rabbit and rabbit.get("enabled"):
        for c in rabbit.get("consumes", {}).get("commands", []):
            q = c["queue"]
            qid = node_id(q)
            lines.append(f'    {qid}([{q}])')
            lines.append(f"    {qid} --> MS")

        for e in rabbit.get("publishes", {}).get("events", []):
            rk = e["routing_key"]
            rid = node_id(rk)
            lines.append(f'    MS --> {rid}["{rk}"]')

    return "\n".join(lines)


# --------------------------------------------------
# Diagram 2 — Architecture / Ports (Hexagonal)
# --------------------------------------------------

def generate_architecture_diagram(svc: dict) -> str:
    arch = svc.get("architecture", {})
    ports = arch.get("ports")

    if not ports:
        return "graph TB\n    MissingArchitecture[Architecture not defined]"

    lines = [
        "graph TB",
        '    Core["Core<br/>Domain & Use Cases"]',
    ]

    for port_name, direction in ports.items():
        pid = node_id(port_name)
        lines.append(f'    {pid}["{port_name}"]')

        if direction == "input":
            lines.append(f"    {pid} --> Core")
        elif direction == "output":
            lines.append(f"    Core --> {pid}")

    return "\n".join(lines)


# --------------------------------------------------
# Diagram 3 — Messaging (RabbitMQ)
# --------------------------------------------------

def generate_messaging_diagram(svc: dict) -> str:
    rabbit = svc.get("interfaces", {}).get("rabbitmq")

    if not rabbit or not rabbit.get("enabled"):
        return "graph TB\n    NoRabbitMQ[RabbitMQ disabled]"

    lines = [
        "graph TB",
        '    MS["Service"]',
    ]

    exchanges = {}
    queues = {}

    # Exchanges
    for ex in rabbit.get("exchanges", []):
        name = ex["name"]
        eid = node_id(name)
        exchanges[name] = eid
        lines.append(f'    {eid}["{name}<br/>({ex["type"]})"]')

    # Queues
    for q in rabbit.get("queues", []):
        name = q["name"]
        qid = node_id(name)
        queues[name] = qid
        lines.append(f'    {qid}([{name}])')

    # Consumes
    for c in rabbit.get("consumes", {}).get("commands", []):
        q = c["queue"]
        if q in queues:
            lines.append(f"    {queues[q]} --> MS")

    # Publishes
    for e in rabbit.get("publishes", {}).get("events", []):
        ex = e["exchange"]
        if ex in exchanges:
            lines.append(f"    MS --> {exchanges[ex]}")

    return "\n".join(lines)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: generate_mermaid.py <service.yaml> <output_dir>")
        sys.exit(1)

    service_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    svc = load_service(service_file)

    write_diagram(output_dir, "service.mmd", generate_service_diagram(svc))
    write_diagram(output_dir, "architecture.mmd", generate_architecture_diagram(svc))
    write_diagram(output_dir, "messaging.mmd", generate_messaging_diagram(svc))


if __name__ == "__main__":
    main()
