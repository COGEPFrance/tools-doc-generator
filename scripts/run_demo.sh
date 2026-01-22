#!/bin/bash

# Script de démonstration pour générer les diagrammes Mermaid

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SERVICE_FILE="../service.yaml"
OUTPUT_DIR="../diagrams"

echo -e "${BLUE}🔍 Génération des diagrammes Mermaid...${NC}"
echo "   Fichier source: $SERVICE_FILE"
echo "   Dossier de sortie: $OUTPUT_DIR"
echo ""

# Vérifier que le fichier source existe
if [ ! -f "$SERVICE_FILE" ]; then
    echo -e "${RED}❌ Erreur: Le fichier $SERVICE_FILE n'existe pas${NC}"
    exit 1
fi

# Lancer la génération
python ../generate_mermaid.py "$SERVICE_FILE" "$OUTPUT_DIR"

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Génération terminée avec succès!${NC}"
    echo ""
    echo "📊 Diagrammes générés:"

    if ls "$OUTPUT_DIR"/*.mmd 1> /dev/null 2>&1; then
        for file in "$OUTPUT_DIR"/*.mmd; do
            size=$(wc -l < "$file")
            echo "   - $(basename "$file") (${size} lignes)"
        done

        echo ""
        echo "💡 Pour visualiser les diagrammes:"
        echo "   - GitHub/GitLab: Commit et push, ils seront rendus automatiquement"
        echo "   - Mermaid Live: https://mermaid.live/"
        echo "   - VSCode: Extension 'Markdown Preview Mermaid Support'"
    else
        echo -e "${RED}   Aucun diagramme généré${NC}"
    fi
else
    echo -e "${RED}❌ Erreur lors de la génération${NC}"
    exit 1
fi
