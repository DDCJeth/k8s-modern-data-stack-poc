"""
Générateur de données CDRs
Génère des fichiers CSV pour Voice, SMS, Data CDR et Cell Towers
Mise à jour : Support pour upload S3 et SFTP
"""

import os
import sys
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


def main():
    """Fonction principale"""
    # Parser les arguments
    # NOTE: Assurez-vous que cli.py est mis à jour pour accepter:
    # --storage (valeurs: 'local', 's3', 'sftp')
    # --bucket (pour s3)
    # --sftp-host, --sftp-user, --sftp-password, --sftp-path (pour sftp)
    args = parse_arguments()
    
    # Valeur par défaut si non spécifié
    if not hasattr(args, 'storage'):
        args.storage = 'local'

    # Créer le répertoire de sortie local (toujours utilisé comme buffer)
    output_dir = ensure_output_dir('cdr_data')

    print("=" * 60)
    print(f"Génération des fichiers CDR (Mode stockage: {args.storage.upper()})")
    print("=" * 60)

    # Convertir la date de début
    start_date = datetime.fromisoformat(START_DATE)

    # 1. Générer Cell Towers (toujours)
    print("\n1. Génération des tours cellulaires...")
    generate_cell_towers_csv(output_dir, CELL_TOWERS, CELL_TOWERS_FIELDNAMES)
    # On n'upload généralement pas le fichier de config statique, mais si besoin :
    # handle_storage(output_dir / 'cell_towers.csv', args)

    # 2. Générer Voice CDR si demandé
    if args.type in ['voice', 'all']:
        records_per_file = args.records if args.records else DEFAULT_VOICE_RECORDS
        print(f"\n2. Génération des Voice CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        for file_num in range(1, args.file + 1):
            current_start = start_date + timedelta(days=file_num-1) # file_num correspond à un jour
            voice_records = generate_voice_cdr(records_per_file, current_start)
            filename = output_dir / f'voice_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
            
            save_to_csv(voice_records, filename, VOICE_CDR_FIELDNAMES)
            handle_storage(filename, args)

    # 3. Générer SMS CDR si demandé
    if args.type in ['sms', 'all']:
        records_per_file = args.records if args.records else DEFAULT_SMS_RECORDS
        print(f"\n3. Génération des SMS CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        for file_num in range(1, args.file + 1):
            current_start = start_date + timedelta(days=file_num-1) # file_num correspond à un jour
            sms_records = generate_sms_cdr(records_per_file, current_start)
            filename = output_dir / f'sms_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
            
            save_to_csv(sms_records, filename, SMS_CDR_FIELDNAMES)
            handle_storage(filename, args)

    # 4. Générer Data CDR si demandé
    if args.type in ['data', 'all']:
        records_per_file = args.records if args.records else DEFAULT_DATA_RECORDS
        print(f"\n4. Génération des Data CDR ({args.file} fichiers de {records_per_file} enregistrements)...")

        for file_num in range(1, args.file + 1):
            current_start = start_date + timedelta(days=file_num-1) # file_num correspond à un jour
            data_records = generate_data_cdr(records_per_file, current_start)
            filename = output_dir / f'data_cdr_{current_start.strftime("%Y%m%d")}_{file_num:02d}.csv'
            
            save_to_csv(data_records, filename, DATA_CDR_FIELDNAMES)
            handle_storage(filename, args)

    # Afficher le résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    if args.type in ['voice', 'all']:
        voice_records_count = args.file * (args.records if args.records else DEFAULT_VOICE_RECORDS)
        print(f"Voice CDR: {voice_records_count} enregistrements ({args.file} fichiers)")
    
    if args.type in ['sms', 'all']:
        sms_records_count = args.file * (args.records if args.records else DEFAULT_SMS_RECORDS)
        print(f"SMS CDR: {sms_records_count} enregistrements ({args.file} fichiers)")
    
    if args.type in ['data', 'all']:
        data_records_count = args.file * (args.records if args.records else DEFAULT_DATA_RECORDS)
        print(f"Data CDR: {data_records_count} enregistrements ({args.file} fichiers)")
    
    print(f"Cell Towers: {len(CELL_TOWERS)} tours")
    print(f"\nFichiers générés localement dans: {output_dir.absolute()}")
    
    if args.storage == 's3':
        print(f"Upload vers S3 Bucket: {args.bucket}")
    elif args.storage == 'sftp':
        print(f"Upload vers SFTP: {args.sftp_host}")
        
    print("=" * 60)


if __name__ == "__main__":
    main()