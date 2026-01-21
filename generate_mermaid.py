#!/usr/bin/env python3

import sys
import yaml
from pathlib import Path


def load_service(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_diagram(output_dir: Path, name: str, content: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / name).write_text(content.strip() + "\n", encoding="utf-8")


# --------------------------------------------------
# Diagram generators
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
    if api:
        api_label = f'HTTP API<br/>{api["base_path"]}'
        lines.append(f'    API["{api_label}"]')
        lines.append("    API --> MS")

    # CLI
    cli = interfaces.get("cli")
    if cli and cli.get("enabled"):
        lines.append('    CLI["CLI"]')
        lines.append("    CLI --> MS")

    # RabbitMQ
    rabbit = interfaces.get("rabbitmq")
    if rabbit and rabbit.get("enabled"):
        consumes = rabbit.get("consumes", {}).get("commands", [])
        publishes = rabbit.get("publishes", {}).get("events", [])

        for c in consumes:
            q = c["queue"]
            lines.append(f'    {q.replace(".", "_")}([{q}])')
            lines.append(f"    {q.replace('.', '_')} --> MS")

        for e in publishes:
            rk = e["routing_key"]
            node = rk.replace(".", "_")
            lines.append(f'    MS --> {node}["{rk}"]')

    return "\n".join(lines)


def generate_architecture_diagram(svc: dict) -> str:
    arch = svc.get("architecture")
    if not arch:
        return "graph TB\n    MissingArchitecture[Architecture not defined]"

    lines = [
        "graph TB",
        '    Core["Core<br/>Domain & Use Cases"]',
    ]

    interfaces = arch.get("interfaces", {})

    for name, cfg in interfaces.items():
        node = name.capitalize()
        lines.append(f'    {node}["{name}"]')

        if isinstance(cfg, dict):
            port = cfg.get("port")
            if port == "input":
                lines.append(f"    {node} --> Core")
            elif port == "output":
                lines.append(f"    Core --> {node}")
        else:
            lines.append(f"    {node} --> Core")

    return "\n".join(lines)


def generate_messaging_diagram(svc: dict) -> str:
    rabbit = svc.get("interfaces", {}).get("rabbitmq")
    if not rabbit or not rabbit.get("enabled"):
        return "graph TB\n    NoRabbitMQ[RabbitMQ disabled]"

    lines = [
        "graph TB",
        '    MS["Service"]',
    ]

    # Exchanges
    exchanges = {}
    for ex in rabbit.get("exchanges", []):
        ex_id = ex["name"].replace(".", "_")
        exchanges[ex["name"]] = ex_id
        lines.append(f'    {ex_id}["{ex["name"]}<br/>({ex["type"]})"]')

    # Queues
    queues = {}
    for q in rabbit.get("queues", []):
        q_id = q.replace(".", "_")
        queues[q] = q_id
        lines.append(f'    {q_id}([{q}])')

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
    service_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    svc = load_service(service_file)

    write_diagram(output_dir, "service.mmd", generate_service_diagram(svc))
    write_diagram(output_dir, "architecture.mmd", generate_architecture_diagram(svc))
    write_diagram(output_dir, "messaging.mmd", generate_messaging_diagram(svc))


if __name__ == "__main__":
    main()
