"""
Générateur de données CDRs
Génère des fichiers CSV pour Voice, SMS, Data CDR et Cell Towers
Mise à jour : Support pour upload S3, SFTP et gestion de l'état (state_generation.txt)
"""

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


def main():
    """Fonction principale"""
    args = parse_arguments()
    
    if not hasattr(args, 'storage'):
        args.storage = 'local'

    output_dir = ensure_output_dir('cdr_data')
    state_file = 'state_generation.txt'
    
    # Charger l'état précédent
    state = load_state(state_file)

    print("=" * 60)
    print(f"Génération des fichiers CDR (Mode stockage: {args.storage.upper()})")
    print("=" * 60)

    # 1. Générer Cell Towers
    print("\n1. Génération des tours cellulaires...")
    generate_cell_towers_csv(output_dir, CELL_TOWERS, CELL_TOWERS_FIELDNAMES)

    # 2. Générer Voice CDR
    if args.type in ['voice', 'all']:
        records_per_file = args.records if args.records else DEFAULT_VOICE_RECORDS
        print(f"\n2. Génération des Voice CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        base_date_str = state['voice']['last_date']
        current_id = state['voice']['last_id']
        base_date = datetime.fromisoformat(base_date_str) if base_date_str else datetime.fromisoformat(START_DATE)

        for file_num in range(1, args.file + 1):
            # Si on reprend depuis un état existant, le premier fichier (file_num=1) commence à +1 jour
            offset = file_num if base_date_str else file_num - 1
            current_start = base_date + timedelta(days=offset)
            
            voice_records = generate_voice_cdr(records_per_file, current_start, start_id=current_id)
            
            if voice_records:
                filename = output_dir / f'voice_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
                save_to_csv(voice_records, filename, VOICE_CDR_FIELDNAMES)
                handle_storage(filename, args)
                
                # Mise à jour de l'état local
                last_record = voice_records[-1]
                state['voice']['last_date'] = last_record['timestamp'].isoformat() if isinstance(last_record['timestamp'], datetime) else str(last_record['timestamp'])
                current_id = extract_id_number(last_record['call_id'])
                state['voice']['last_id'] = current_id

    # 3. Générer SMS CDR
    if args.type in ['sms', 'all']:
        records_per_file = args.records if args.records else DEFAULT_SMS_RECORDS
        print(f"\n3. Génération des SMS CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        base_date_str = state['sms']['last_date']
        current_id = state['sms']['last_id']
        base_date = datetime.fromisoformat(base_date_str) if base_date_str else datetime.fromisoformat(START_DATE)

        for file_num in range(1, args.file + 1):
            offset = file_num if base_date_str else file_num - 1
            current_start = base_date + timedelta(days=offset)
            
            sms_records = generate_sms_cdr(records_per_file, current_start, start_id=current_id)
            
            if sms_records:
                filename = output_dir / f'sms_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
                save_to_csv(sms_records, filename, SMS_CDR_FIELDNAMES)
                handle_storage(filename, args)
                
                # Mise à jour de l'état local
                last_record = sms_records[-1]
                state['sms']['last_date'] = last_record['timestamp'].isoformat() if isinstance(last_record['timestamp'], datetime) else str(last_record['timestamp'])
                current_id = extract_id_number(last_record['sms_id'])
                state['sms']['last_id'] = current_id

    # 4. Générer Data CDR
    if args.type in ['data', 'all']:
        records_per_file = args.records if args.records else DEFAULT_DATA_RECORDS
        print(f"\n4. Génération des Data CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        base_date_str = state['data']['last_date']
        current_id = state['data']['last_id']
        base_date = datetime.fromisoformat(base_date_str) if base_date_str else datetime.fromisoformat(START_DATE)

        for file_num in range(1, args.file + 1):
            offset = file_num if base_date_str else file_num - 1
            current_start = base_date + timedelta(days=offset)
            
            data_records = generate_data_cdr(records_per_file, current_start, start_id=current_id)
            
            if data_records:
                filename = output_dir / f'data_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
                save_to_csv(data_records, filename, DATA_CDR_FIELDNAMES)
                handle_storage(filename, args)
                
                # Mise à jour de l'état local
                last_record = data_records[-1]
                state['data']['last_date'] = last_record['timestamp'].isoformat() if isinstance(last_record['timestamp'], datetime) else str(last_record['timestamp'])
                current_id = extract_id_number(last_record['session_id'])
                state['data']['last_id'] = current_id

    # Sauvegarder l'état global à la fin de l'exécution
    save_state(state, state_file)

    # Afficher le résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    # ... (Le code du résumé reste inchangé) ...
    
    print(f"\nÉtat de la génération sauvegardé dans : {state_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()