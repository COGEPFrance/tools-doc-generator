import sys
import yaml
from pathlib import Path

# Args
service_file = sys.argv[1]
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

with open(service_file) as f:
    svc = yaml.safe_load(f)

name = svc["service"]["name"]
version = svc["service"]["version"]

lines = []
lines.append("graph TB")
lines.append(f'    MS["{name}<br/>v{version}"]')

interfaces = svc.get("interfaces", {})

# API
if "api" in interfaces:
    api = interfaces["api"]
    lines.append(f'    API["HTTP API<br/>{api["base_path"]}"]')
    lines.append("    API --> MS")

# CLI
if interfaces.get("cli", {}).get("enabled"):
    lines.append('    CLI["CLI"]')
    lines.append("    CLI --> MS")

# RabbitMQ
rabbit = interfaces.get("rabbitmq", {})
if rabbit.get("enabled"):
    for c in rabbit.get("consumes", {}).get("commands", []):
        q = c["queue"]
        q_id = q.replace(".", "_")
        lines.append(f'    {q_id}([{q}])')
        lines.append(f'    {q_id} --> MS')

    for e in rabbit.get("publishes", {}).get("events", []):
        rk = e["routing_key"]
        rk_id = rk.replace(".", "_")
        lines.append(f'    MS --> {rk_id}["{rk}"]')

# Write file
output_file = output_dir / "service.mmd"
output_file.write_text("\n".join(lines), encoding="utf-8")

print(f"Mermaid diagram written to {output_file}")
