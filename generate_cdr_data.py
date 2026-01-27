"""
Générateur de données CDR pour Orange Mali
Génère des fichiers CSV pour Voice, SMS, Data CDR et Cell Towers
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Régions du Mali
REGIONS = [
    'Bamako', 'Segou', 'Sikasso', 'Kayes',
    'Mopti', 'Tombouctou', 'Gao', 'Kidal'
]

# Configuration des cellules par région
CELL_TOWERS = [
    {'cell_id': 'CELL_BAM_001', 'region': 'Bamako', 'province': 'Bamako Capital', 'latitude': 12.6392, 'longitude': -8.0029, 'technology': '4G', 'capacity_erlang': 150},
    {'cell_id': 'CELL_BAM_002', 'region': 'Bamako', 'province': 'Bamako Capital', 'latitude': 12.6500, 'longitude': -7.9900, 'technology': '4G', 'capacity_erlang': 180},
    {'cell_id': 'CELL_BAM_003', 'region': 'Bamako', 'province': 'Bamako Capital', 'latitude': 12.6200, 'longitude': -8.0200, 'technology': '3G', 'capacity_erlang': 100},
    {'cell_id': 'CELL_SEG_001', 'region': 'Segou', 'province': 'Segou', 'latitude': 13.4317, 'longitude': -6.2664, 'technology': '4G', 'capacity_erlang': 120},
    {'cell_id': 'CELL_SIK_001', 'region': 'Sikasso', 'province': 'Sikasso', 'latitude': 11.3177, 'longitude': -5.6661, 'technology': '3G', 'capacity_erlang': 80},
    {'cell_id': 'CELL_KAY_001', 'region': 'Kayes', 'province': 'Kayes', 'latitude': 14.4474, 'longitude': -11.4448, 'technology': '3G', 'capacity_erlang': 70},
    {'cell_id': 'CELL_MOP_001', 'region': 'Mopti', 'province': 'Mopti', 'latitude': 14.4844, 'longitude': -4.1966, 'technology': '4G', 'capacity_erlang': 90},
    {'cell_id': 'CELL_TOM_001', 'region': 'Tombouctou', 'province': 'Tombouctou', 'latitude': 16.7734, 'longitude': -3.0074, 'technology': '3G', 'capacity_erlang': 60},
    {'cell_id': 'CELL_GAO_001', 'region': 'Gao', 'province': 'Gao', 'latitude': 16.2719, 'longitude': -0.0447, 'technology': '3G', 'capacity_erlang': 50},
    {'cell_id': 'CELL_KID_001', 'region': 'Kidal', 'province': 'Kidal', 'latitude': 18.4411, 'longitude': 1.4078, 'technology': '2G', 'capacity_erlang': 30},
]

# Types d'appels
CALL_TYPES = ['MOC', 'MTC']  # Mobile Originated Call, Mobile Terminated Call
TERMINATION_REASONS = ['NORMAL', 'FAILED', 'USER_TERMINATED', 'NO_ANSWER', 'NETWORK_ERROR']

# Types de SMS
SMS_TYPES = ['MO', 'MT']  # Mobile Originated, Mobile Terminated
SMS_DELIVERY_STATUS = ['DELIVERED', 'FAILED', 'PENDING']

# Configuration Data
APN_TYPES = ['internet.mali', 'mms.mali', 'wap.mali']
SESSION_END_REASONS = ['NORMAL', 'USER_TERMINATED', 'QUOTA_EXCEEDED', 'NETWORK_ERROR', 'TIMEOUT']


def generate_msisdn():
    """Génère un numéro MSISDN malien (format: 223 + 8 chiffres)"""
    prefix = random.choice(['70', '71', '72', '73', '74', '75', '76', '77', '78', '79'])
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"223{prefix}{suffix}"


def generate_voice_cdr(num_records, start_time):
    """Génère des enregistrements Voice CDR"""
    records = []
    current_time = start_time

    for i in range(num_records):
        call_type = random.choice(CALL_TYPES)
        cell_tower = random.choice(CELL_TOWERS)

        # Probabilité de succès plus élevée
        termination_reason = random.choices(
            TERMINATION_REASONS,
            weights=[80, 5, 5, 5, 5],  # 80% NORMAL
            k=1
        )[0]

        # Durée et montant basés sur le statut
        if termination_reason == 'NORMAL':
            duration = random.randint(30, 1800)  # 30 sec à 30 min
            charging_amount = round(duration * 0.5, 1) if call_type == 'MOC' else 0.0
        elif termination_reason == 'USER_TERMINATED':
            duration = random.randint(10, 300)
            charging_amount = round(duration * 0.5, 1) if call_type == 'MOC' else 0.0
        else:
            duration = 0
            charging_amount = 0.0

        record = {
            'timestamp': current_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'call_id': f"CALL_{i+1:06d}",
            'caller_msisdn': generate_msisdn(),
            'callee_msisdn': generate_msisdn(),
            'call_type': call_type,
            'duration_seconds': duration,
            'cell_id': cell_tower['cell_id'],
            'region': cell_tower['region'],
            'termination_reason': termination_reason,
            'charging_amount': charging_amount
        }
        records.append(record)

        # Incrémenter le temps de manière aléatoire
        current_time += timedelta(seconds=random.randint(1, 30))

    return records


def generate_sms_cdr(num_records, start_time):
    """Génère des enregistrements SMS CDR"""
    records = []
    current_time = start_time

    for i in range(num_records):
        sms_type = random.choice(SMS_TYPES)
        cell_tower = random.choice(CELL_TOWERS)

        # Probabilité de succès très élevée pour SMS
        delivery_status = random.choices(
            SMS_DELIVERY_STATUS,
            weights=[90, 5, 5],  # 90% DELIVERED
            k=1
        )[0]

        message_length = random.randint(10, 160)

        # Montant basé sur le statut et le type
        if delivery_status == 'DELIVERED' and sms_type == 'MO':
            charging_amount = 25.0
        else:
            charging_amount = 0.0

        record = {
            'timestamp': current_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'sms_id': f"SMS_{i+1:06d}",
            'sender_msisdn': generate_msisdn(),
            'receiver_msisdn': generate_msisdn(),
            'sms_type': sms_type,
            'message_length': message_length,
            'cell_id': cell_tower['cell_id'],
            'region': cell_tower['region'],
            'delivery_status': delivery_status,
            'charging_amount': charging_amount
        }
        records.append(record)

        # Incrémenter le temps
        current_time += timedelta(seconds=random.randint(1, 20))

    return records


def generate_data_cdr(num_records, start_time):
    """Génère des enregistrements Data CDR"""
    records = []
    current_time = start_time

    for i in range(num_records):
        cell_tower = random.choice(CELL_TOWERS)
        apn = random.choice(APN_TYPES)

        # Probabilité de session normale élevée
        session_end_reason = random.choices(
            SESSION_END_REASONS,
            weights=[85, 5, 5, 3, 2],  # 85% NORMAL
            k=1
        )[0]

        # Durée de session
        if session_end_reason == 'NORMAL':
            session_duration = random.randint(300, 7200)  # 5 min à 2h
        elif session_end_reason == 'USER_TERMINATED':
            session_duration = random.randint(60, 1800)
        else:
            session_duration = random.randint(10, 300)

        # Volume de données
        if apn == 'internet.mali':
            bytes_uploaded = random.randint(1048576, 104857600)  # 1 MB à 100 MB
            bytes_downloaded = random.randint(10485760, 1048576000)  # 10 MB à 1 GB
            charging_rate = 0.0002  # 0.2 FCFA par KB
        elif apn == 'mms.mali':
            bytes_uploaded = random.randint(524288, 10485760)  # 512 KB à 10 MB
            bytes_downloaded = random.randint(1048576, 20971520)  # 1 MB à 20 MB
            charging_rate = 0.0001
        else:  # wap.mali
            bytes_uploaded = random.randint(524288, 5242880)  # 512 KB à 5 MB
            bytes_downloaded = random.randint(2097152, 52428800)  # 2 MB à 50 MB
            charging_rate = 0.00015

        total_bytes = bytes_uploaded + bytes_downloaded
        charging_amount = round((total_bytes / 1024) * charging_rate, 1) if session_end_reason == 'NORMAL' else 0.0

        record = {
            'timestamp': current_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'session_id': f"DATA_{i+1:06d}",
            'msisdn': generate_msisdn(),
            'apn': apn,
            'session_duration_seconds': session_duration,
            'bytes_uploaded': bytes_uploaded,
            'bytes_downloaded': bytes_downloaded,
            'cell_id': cell_tower['cell_id'],
            'region': cell_tower['region'],
            'session_end_reason': session_end_reason,
            'charging_amount': charging_amount
        }
        records.append(record)

        # Incrémenter le temps
        current_time += timedelta(seconds=random.randint(30, 180))

    return records


def save_to_csv(records, filename, fieldnames):
    """Sauvegarde les enregistrements dans un fichier CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"✓ Généré: {filename} ({len(records)} enregistrements)")


def generate_cell_towers_csv(output_dir):
    """Génère le fichier CSV des tours cellulaires"""
    filename = output_dir / 'cell_towers_mali.csv'
    fieldnames = ['cell_id', 'region', 'province', 'latitude', 'longitude', 'technology', 'capacity_erlang']

    save_to_csv(CELL_TOWERS, filename, fieldnames)


def main():
    """Fonction principale"""
    # Créer le répertoire de sortie
    output_dir = Path('cdr_data')
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Génération des fichiers CDR pour Orange Mali")
    print("=" * 60)

    # Date de début
    start_date = datetime(2024, 12, 14, 8, 0, 0)

    # 1. Générer Cell Towers
    print("\n1. Génération des tours cellulaires...")
    generate_cell_towers_csv(output_dir)

    # 2. Générer Voice CDR (100,000 records - 10 fichiers de 10,000)
    print("\n2. Génération des Voice CDR...")
    voice_fieldnames = ['timestamp', 'call_id', 'caller_msisdn', 'callee_msisdn',
                        'call_type', 'duration_seconds', 'cell_id', 'region',
                        'termination_reason', 'charging_amount']

    for file_num in range(1, 11):
        current_start = start_date + timedelta(hours=file_num-1)
        voice_records = generate_voice_cdr(10000, current_start)
        filename = output_dir / f'voice_cdr_mali_{file_num:02d}.csv'
        save_to_csv(voice_records, filename, voice_fieldnames)

    # 3. Générer SMS CDR (50,000 records - 10 fichiers de 5,000)
    print("\n3. Génération des SMS CDR...")
    sms_fieldnames = ['timestamp', 'sms_id', 'sender_msisdn', 'receiver_msisdn',
                      'sms_type', 'message_length', 'cell_id', 'region',
                      'delivery_status', 'charging_amount']

    for file_num in range(1, 11):
        current_start = start_date + timedelta(hours=file_num-1)
        sms_records = generate_sms_cdr(5000, current_start)
        filename = output_dir / f'sms_cdr_mali_{file_num:02d}.csv'
        save_to_csv(sms_records, filename, sms_fieldnames)

    # 4. Générer Data CDR (30,000 records - 10 fichiers de 3,000)
    print("\n4. Génération des Data CDR...")
    data_fieldnames = ['timestamp', 'session_id', 'msisdn', 'apn',
                       'session_duration_seconds', 'bytes_uploaded', 'bytes_downloaded',
                       'cell_id', 'region', 'session_end_reason', 'charging_amount']

    for file_num in range(1, 11):
        current_start = start_date + timedelta(hours=file_num-1)
        data_records = generate_data_cdr(3000, current_start)
        filename = output_dir / f'data_cdr_mali_{file_num:02d}.csv'
        save_to_csv(data_records, filename, data_fieldnames)

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"Total Voice CDR: 100,000 enregistrements (10 fichiers)")
    print(f"Total SMS CDR: 50,000 enregistrements (10 fichiers)")
    print(f"Total Data CDR: 30,000 enregistrements (10 fichiers)")
    print(f"Cell Towers: {len(CELL_TOWERS)} tours")
    print(f"\nTous les fichiers ont été générés dans le répertoire: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
