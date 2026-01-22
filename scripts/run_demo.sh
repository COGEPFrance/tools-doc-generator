#!/bin/bash

# Script de démonstration pour générer les diagrammes Mermaid

SERVICE_FILE="${1:-service.yaml}"
OUTPUT_DIR="${2:-diagrams}"

echo "🔍 Génération des diagrammes Mermaid..."
echo "   Fichier source: $SERVICE_FILE"
echo "   Dossier de sortie: $OUTPUT_DIR"
echo ""

python generate_mermaid.py "$SERVICE_FILE" "$OUTPUT_DIR"

echo ""
echo "✅ Génération terminée!"
echo ""
echo "📊 Diagrammes générés:"
ls -lh "$OUTPUT_DIR"/*.mmd 2>/dev/null || echo "   Aucun diagramme généré"
