import yaml

with open("service.yaml") as f:
    svc = yaml.safe_load(f)

name = svc["service"]["name"]
version = svc["service"]["version"]

lines = ["graph TB", f'    MS["{name}<br/>v{version}"]']

# API
if "api" in svc["interfaces"]:
    api = svc["interfaces"]["api"]
    lines.append(f'    API["HTTP API<br/>{api["base_path"]}"]')
    lines.append("    API --> MS")

# CLI
if svc["interfaces"].get("cli", {}).get("enabled"):
    lines.append('    CLI["CLI"]')
    lines.append("    CLI --> MS")

# RabbitMQ
rabbit = svc["interfaces"].get("rabbitmq", {})
if rabbit.get("enabled"):
    for c in rabbit.get("consumes", {}).get("commands", []):
        q = c["queue"]
        lines.append(f'    {q.replace(".", "_")}([{q}])')
        lines.append(f'    {q.replace(".", "_")} --> MS')

    for e in rabbit.get("publishes", {}).get("events", []):
        rk = e["routing_key"].replace(".", "_")
        lines.append(f'    MS --> {rk}["{e["routing_key"]}"]')

print("\n".join(lines))
