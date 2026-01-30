"""
Générateurs de CDR (Voice, SMS, Data)
"""

import random
from datetime import timedelta
from config import (
    CELL_TOWERS, CALL_TYPES, TERMINATION_REASONS, SMS_TYPES, SMS_DELIVERY_STATUS,
    APN_TYPES, SESSION_END_REASONS
)


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
