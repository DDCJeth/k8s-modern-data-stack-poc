"""
Générateur de données CDRs en mode streaming
Génère les fichiers CSV en continu à intervalles aléatoires jusqu'à l'arrêt de l'utilisateur
Mise à jour : Gestion de l'état (state_generation.txt) pour reprendre là où on s'est arrêté
"""

import os
import time
import random
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from cli import parse_arguments
from config import (
    CELL_TOWERS, START_DATE, VOICE_CDR_FIELDNAMES, SMS_CDR_FIELDNAMES,
    DATA_CDR_FIELDNAMES, CELL_TOWERS_FIELDNAMES, DEFAULT_VOICE_RECORDS,
    DEFAULT_SMS_RECORDS, DEFAULT_DATA_RECORDS
)
from generators import generate_voice_cdr, generate_sms_cdr, generate_data_cdr
from utils import save_to_csv, generate_cell_towers_csv, ensure_output_dir, upload_to_s3, upload_to_sftp, handle_storage, load_state, save_state, extract_id_number


def get_generator_config(cdr_type):
    """Retourne la configuration du générateur pour un type de CDR"""
    config = {
        'voice': {
            'generator': generate_voice_cdr,
            'fieldnames': VOICE_CDR_FIELDNAMES,
            'default_records': DEFAULT_VOICE_RECORDS,
            'filename_pattern': 'voice_cdr_{}_{:02d}.csv',
            'id_field': 'call_id'
        },
        'sms': {
            'generator': generate_sms_cdr,
            'fieldnames': SMS_CDR_FIELDNAMES,
            'default_records': DEFAULT_SMS_RECORDS,
            'filename_pattern': 'sms_cdr_{}_{:02d}.csv',
            'id_field': 'sms_id'
        },
        'data': {
            'generator': generate_data_cdr,
            'fieldnames': DATA_CDR_FIELDNAMES,
            'default_records': DEFAULT_DATA_RECORDS,
            'filename_pattern': 'data_cdr_{}_{:02d}.csv',
            'id_field': 'session_id'
        }
    }
    return config.get(cdr_type)


def main():
    """Fonction principale - Mode streaming"""
    args = parse_arguments()
    
    # Vérifier que min_delay < max_delay
    if args.min_delay >= args.max_delay:
        print(f"Erreur: --min-delay ({args.min_delay}s) doit être inférieur à --max-delay ({args.max_delay}s)")
        return
    
    output_dir = ensure_output_dir('cdr_data')
    state_file = 'state_generation.txt'

    # Réinitialisation de l'état si demandé
    if hasattr(args, 'reset_state') and args.reset_state and os.path.exists(state_file):
        os.remove(state_file)
        print(f"🔄 Option --reset-state activée : Le fichier {state_file} a été réinitialisé.")

    # Charger l'état
    state = load_state(state_file)

    print("=" * 70)
    print("Générateur CDR - Mode Streaming")
    print("=" * 70)
    print(f"Type de CDR: {args.type}")
    print(f"Enregistrements par fichier: {args.records or 'défaut'}")
    print(f"Délai entre générations: {args.min_delay}s - {args.max_delay}s")
    print(f"Répertoire de sortie: {output_dir.absolute()}")
    print("\nAppuyez sur Ctrl+C pour arrêter le générateur")
    print("=" * 70 + "\n")
    
    # Générer Cell Towers une seule fois
    print("Génération des tours cellulaires...")
    generate_cell_towers_csv(output_dir, CELL_TOWERS, CELL_TOWERS_FIELDNAMES)
    
    # Compteur de fichiers générés durant CETTE session
    file_counters = {'voice': 0, 'sms': 0, 'data': 0}
    cdr_types = [args.type] if args.type != 'all' else ['voice', 'sms', 'data']
    
    try:
        while True:
            current_type = random.choice(cdr_types) if args.type == 'all' else args.type
            config = get_generator_config(current_type)
            
            # Récupérer l'état actuel pour ce type
            last_date_str = state[current_type]['last_date']
            current_id = state[current_type]['last_id']
            
            # Déterminer la date du prochain fichier
            if last_date_str:
                current_start = datetime.fromisoformat(last_date_str) + timedelta(days=1)
            else:
                current_start = datetime.fromisoformat(START_DATE)

            records_per_file = args.records if args.records else config['default_records']
            
            # Incrémenter le compteur de session
            file_counters[current_type] += 1
            file_num = file_counters[current_type] # Utilisé juste pour le nommage local dans cette session
            
            # Générer les données
            cdr_records = config['generator'](records_per_file, current_start, start_id=current_id)
            
            if cdr_records:
                # Sauvegarder en CSV
                filename = output_dir / config['filename_pattern'].format(current_start.strftime("%Y%m%d"), file_num)
                save_to_csv(cdr_records, filename, config['fieldnames'])
                handle_storage(filename, args)
                
                # Mise à jour et sauvegarde de l'état
                last_record = cdr_records[-1]
                state[current_type]['last_date'] = last_record['timestamp'].isoformat() if isinstance(last_record['timestamp'], datetime) else str(last_record['timestamp'])
                state[current_type]['last_id'] = extract_id_number(last_record[config['id_field']])
                save_state(state, state_file)
            
            # Afficher les statistiques actuelles
            total_generated = sum(file_counters.values())
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Total généré (session): {total_generated} fichiers | Voice: {file_counters['voice']}, SMS: {file_counters['sms']}, Data: {file_counters['data']}")
            
            # Attendre avant la prochaine génération
            delay = random.randint(args.min_delay, args.max_delay)
            print(f"Prochain fichier dans {delay} secondes...\n")
            time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Arrêt du générateur CDR")
        print("=" * 70)
        print("RÉSUMÉ DE LA SESSION")
        print("=" * 70)
        print(f"Voice CDR: {file_counters['voice']} fichiers générés")
        print(f"SMS CDR: {file_counters['sms']} fichiers générés")
        print(f"Data CDR: {file_counters['data']} fichiers générés")
        print(f"Total session: {sum(file_counters.values())} fichiers générés")
        print(f"État sauvegardé dans : {state_file}")
        print("=" * 70)

if __name__ == "__main__":
    main()