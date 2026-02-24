"""
Générateurs de CDR (Voice, SMS, Data)
"""

import random
from datetime import datetime, timedelta
from config import (
    CELL_TOWERS, CALL_TYPES, TERMINATION_REASONS, SMS_TYPES, SMS_DELIVERY_STATUS,
    APN_TYPES, SESSION_END_REASONS
)

def generate_random_uniform_times(date_input, n_records):
    """
    Génère n_records timestamps uniformément répartis aléatoirement
    sur une journée donnée.
    Retourne un générateur de tuples (numero, timestamp).
    """

    # Conversion si string
    if isinstance(date_input, str):
        start = datetime.strptime(date_input, "%Y-%m-%d")
    else:
        start = datetime(date_input.year, date_input.month, date_input.day)

    total_seconds = 24 * 60 * 60  # 86400 secondes dans une journée (corrigé de 84400)

    # Tirage uniforme des secondes
    random_seconds = sorted(random.uniform(0, total_seconds) for _ in range(n_records))

    for idx, sec in enumerate(random_seconds, start=1):
        current_time = start + timedelta(seconds=sec)
        yield idx, current_time.strftime("%Y-%m-%dT%H:%M:%S")


import csv

def generate_msisdns(limit=1000):
    """Génère une liste de numéros MSISDN maliens uniques."""
    prefixes = ['70', '71', '72', '73', '74', '75', '76', '77', '78', '79']
    msisdns = set()
    
    while len(msisdns) < limit:
        prefix = random.choice(prefixes)
        suffix = f"{random.randint(0, 999999):06d}"
        msisdns.add(f"223{prefix}{suffix}")
        
    return list(msisdns)


def generate_profil_subscribers(filename="cdr_data/Subscribers.csv", limit=1000):
    """Crée un fichier CSV avec une liste unique de 35 noms/prénoms sans doublon de mots."""
    
    msisdns = generate_msisdns(limit)
    
    # Liste unique de 35 éléments (mélange de noms et prénoms)
    noms_et_prenoms = [
        'Traoré', 'Amadou', 'Diarra', 'Oumar', 'Keita', 'Fatoumata', 
        'Diallo', 'Mariam', 'Touré', 'Awa', 'Cissé', 'Seydou', 
        'Coulibaly', 'Ibrahim', 'Kanté', 'Aminata', 'Dembélé', 'Moussa', 
        'Koné', 'Adama', 'Sangaré', 'Ousmane', 'Sidibé', 'Aïcha', 
        'Sylla', 'Salif', 'Sissoko', 'Habib', 'Camara', 'Kadiatou',
        'Sow', 'Binta', 'Maïga', 'Aliou', 'Fofana' # Les 5 nouveaux ajouts
    ]
    
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2005, 12, 31)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['MSISDN', 'Nom', 'Prénom', 'Date de Naissance', 'Email'])
        
        for msisdn in msisdns:
            # random.sample(liste, 2) tire 2 éléments distincts de la liste
            # Cela garantit que nom et prenom seront toujours deux mots différents
            nom, prenom = random.sample(noms_et_prenoms, 2)
            
            random_days = random.randint(0, (end_date - start_date).days)
            dob = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
            
            # Nettoyage pour les emails (gestion des trémas et accents)
            clean_nom = nom.replace('é', 'e').replace('ï', 'i').lower()
            clean_prenom = prenom.replace('é', 'e').replace('ï', 'i').lower()
            email = f"{clean_prenom}.{clean_nom}{random.randint(10, 99)}@example.com"
            
            writer.writerow([msisdn, nom, prenom, dob, email])
            
    print(f"Succès ! Le fichier '{filename}' a été créé avec {limit} abonnés uniques.")




def generate_voice_cdr(num_records, start_time, start_id=0):
    """Génère des enregistrements Voice CDR"""
    records = []

    for i, current_time in generate_random_uniform_times(start_time, num_records):
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
            'timestamp': current_time,
            'call_id': f"CALL_{start_id + i:06d}",
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

    return records


def generate_sms_cdr(num_records, start_time, start_id=0):
    """Génère des enregistrements SMS CDR"""
    records = []

    for i, current_time in generate_random_uniform_times(start_time, num_records):
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
            'timestamp': current_time,
            'sms_id': f"SMS_{start_id + i:06d}",
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

    return records


def generate_data_cdr(num_records, start_time, start_id=0):
    """Génère des enregistrements Data CDR"""
    records = []

    for i, current_time in generate_random_uniform_times(start_time, num_records):
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
            'timestamp': current_time,
            'session_id': f"DATA_{start_id + i:06d}",
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

    return records