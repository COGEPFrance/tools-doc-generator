# Utilisation Locale

## Prérequis

- Python 3.13
- PyYAML

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Méthode 1 : Script direct

```bash
python generate_mermaid.py service.yaml diagrams
```

### Méthode 2 : Script de démonstration

```bash
./run_demo.sh [service.yaml] [output_dir]
```

Par défaut, utilise `service.yaml` et génère les diagrammes dans le dossier `diagrams/`.

## Résultats

Les diagrammes suivants seront générés :

1. **architecture.mmd** : Diagramme de l'architecture hexagonale avec les ports input/output
2. **messaging.mmd** : Diagramme de la configuration RabbitMQ (exchanges, queues, routing)

## Exemple

```bash
# Générer les diagrammes avec le fichier par défaut
./run_demo.sh

# Générer avec un fichier spécifique
./run_demo.sh my-service.yaml output/

# Visualiser les résultats
cat diagrams/architecture.mmd
cat diagrams/messaging.mmd
```

## Architecture du Code

```
.
├── config.py                    # Configuration centralisée
├── ports.py                     # Interfaces (Ports)
├── domain/                      # Logique métier
│   ├── diagram_generator.py    # Interface abstraite
│   ├── node_id_generator.py    # Génération d'IDs
│   ├── architecture_diagram_generator.py
│   └── messaging_diagram_generator.py
├── adapters/                    # Adaptateurs
│   ├── yaml_loader.py          # Chargement YAML
│   └── filesystem_writer.py    # Écriture fichiers
├── application/                 # Couche application
│   └── orchestrator.py         # Orchestration
└── generate_mermaid.py         # Point d'entrée CLI
```

## Principes de Codage

Le code suit les principes :
- **SOLID** : Séparation des responsabilités, injection de dépendances
- **DDD** : Architecture hexagonale avec ports et adapters
- **DRY** : Pas de duplication de code
- **KISS** : Code simple et maintenable
