"""
Générateur de données CDRs en mode streaming
Génère les fichiers CSV en continu à intervalles aléatoires jusqu'à l'arrêt de l'utilisateur
"""

import time
import random
from datetime import datetime, timedelta
from pathlib import Path

from cli import parse_arguments
from config import (
    CELL_TOWERS, START_DATE, VOICE_CDR_FIELDNAMES, SMS_CDR_FIELDNAMES,
    DATA_CDR_FIELDNAMES, CELL_TOWERS_FIELDNAMES, DEFAULT_VOICE_RECORDS,
    DEFAULT_SMS_RECORDS, DEFAULT_DATA_RECORDS
)
from generators import generate_voice_cdr, generate_sms_cdr, generate_data_cdr
from utils import save_to_csv, generate_cell_towers_csv, ensure_output_dir, upload_to_s3, upload_to_sftp, handle_storage


def get_generator_config(cdr_type):
    """Retourne la configuration du générateur pour un type de CDR"""
    config = {
        'voice': {
            'generator': generate_voice_cdr,
            'fieldnames': VOICE_CDR_FIELDNAMES,
            'default_records': DEFAULT_VOICE_RECORDS,
            'filename_pattern': 'voice_cdr_{}_{:02d}.csv'
        },
        'sms': {
            'generator': generate_sms_cdr,
            'fieldnames': SMS_CDR_FIELDNAMES,
            'default_records': DEFAULT_SMS_RECORDS,
            'filename_pattern': 'sms_cdr_{}_{:02d}.csv'
        },
        'data': {
            'generator': generate_data_cdr,
            'fieldnames': DATA_CDR_FIELDNAMES,
            'default_records': DEFAULT_DATA_RECORDS,
            'filename_pattern': 'data_cdr_{}_{:02d}.csv'
        }
    }
    return config.get(cdr_type)


def main():
    """Fonction principale - Mode streaming"""
    # Parser les arguments
    args = parse_arguments()
    
    # Vérifier que min_delay < max_delay
    if args.min_delay >= args.max_delay:
        print(f"Erreur: --min-delay ({args.min_delay}s) doit être inférieur à --max-delay ({args.max_delay}s)")
        return
    
    # Créer le répertoire de sortie
    output_dir = ensure_output_dir('cdr_data')

    print("=" * 70)
    print("Générateur CDR - Mode Streaming")
    print("=" * 70)
    print(f"Type de CDR: {args.type}")
    print(f"Enregistrements par fichier: {args.records or 'défaut'}")
    print(f"Délai entre générations: {args.min_delay}s - {args.max_delay}s")
    print(f"Répertoire de sortie: {output_dir.absolute()}")
    print("\nAppuyez sur Ctrl+C pour arrêter le générateur")
    print("=" * 70 + "\n")

    # Convertir la date de début
    start_date = datetime.fromisoformat(START_DATE)
    
    # Générer Cell Towers une seule fois
    print("Génération des tours cellulaires...")
    generate_cell_towers_csv(output_dir, CELL_TOWERS, CELL_TOWERS_FIELDNAMES)
    
    # Compteur de fichiers générés
    file_counters = {'voice': 0, 'sms': 0, 'data': 0}
    
    # Types de CDR à générer
    cdr_types = [args.type] if args.type != 'all' else ['voice', 'sms', 'data']
    
    try:
        while True:
            # Sélectionner un type aléatoire si 'all' est spécifié
            if args.type == 'all':
                current_type = random.choice(cdr_types)
            else:
                current_type = args.type
            
            # Obtenir la configuration du générateur
            config = get_generator_config(current_type)
            
            # Incrémenter le compteur
            file_counters[current_type] += 1
            file_num = file_counters[current_type]
            
            # Déterminer le nombre d'enregistrements
            records_per_file = args.records if args.records else config['default_records']
            
            # Générer les données
            current_start = start_date + timedelta(days=file_num-1)
            cdr_records = config['generator'](records_per_file, current_start)
            
            # Sauvegarder en CSV
            filename = output_dir / config['filename_pattern'].format(current_start.strftime("%Y%m%d"), file_num)
            save_to_csv(cdr_records, filename, config['fieldnames'])
            handle_storage(filename, args)
            
            # Afficher les statistiques actuelles
            total_generated = sum(file_counters.values())
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Total généré: {total_generated} fichiers | Voice: {file_counters['voice']}, SMS: {file_counters['sms']}, Data: {file_counters['data']}")
            
            # Attendre avant la prochaine génération
            delay = random.randint(args.min_delay, args.max_delay)
            print(f"Prochain fichier dans {delay} secondes...\n")
            time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Arrêt du générateur CDR")
        print("=" * 70)
        print("RÉSUMÉ FINAL")
        print("=" * 70)
        print(f"Voice CDR: {file_counters['voice']} fichiers générés")
        print(f"SMS CDR: {file_counters['sms']} fichiers générés")
        print(f"Data CDR: {file_counters['data']} fichiers générés")
        print(f"Total: {sum(file_counters.values())} fichiers générés")
        print(f"Répertoire: {output_dir.absolute()}")
        print("=" * 70)


if __name__ == "__main__":
    main()


