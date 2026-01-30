"""
Utilitaires pour le générateur de CDR
"""

import csv
from pathlib import Path


def save_to_csv(records, filename, fieldnames):
    """Sauvegarde les enregistrements dans un fichier CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"✓ Généré: {filename} ({len(records)} enregistrements)")


def generate_cell_towers_csv(output_dir, cell_towers, fieldnames):
    """Génère le fichier CSV des tours cellulaires"""
    filename = output_dir / 'cell_towers_mali.csv'
    save_to_csv(cell_towers, filename, fieldnames)


def ensure_output_dir(output_dir_path):
    """Crée le répertoire de sortie s'il n'existe pas"""
    output_dir = Path(output_dir_path)
    output_dir.mkdir(exist_ok=True)
    return output_dir
