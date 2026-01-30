"""
Configuration et constantes pour le générateur de CDR
"""

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

# Date de début pour la génération
START_DATE = '2024-12-14T08:00:00'

# Champs CSV
VOICE_CDR_FIELDNAMES = [
    'timestamp', 'call_id', 'caller_msisdn', 'callee_msisdn',
    'call_type', 'duration_seconds', 'cell_id', 'region',
    'termination_reason', 'charging_amount'
]

SMS_CDR_FIELDNAMES = [
    'timestamp', 'sms_id', 'sender_msisdn', 'receiver_msisdn',
    'sms_type', 'message_length', 'cell_id', 'region',
    'delivery_status', 'charging_amount'
]

DATA_CDR_FIELDNAMES = [
    'timestamp', 'session_id', 'msisdn', 'apn',
    'session_duration_seconds', 'bytes_uploaded', 'bytes_downloaded',
    'cell_id', 'region', 'session_end_reason', 'charging_amount'
]

CELL_TOWERS_FIELDNAMES = [
    'cell_id', 'region', 'province', 'latitude', 'longitude', 'technology', 'capacity_erlang'
]

# Tailles par défaut
DEFAULT_VOICE_RECORDS = 10000
DEFAULT_SMS_RECORDS = 5000
DEFAULT_DATA_RECORDS = 3000
DEFAULT_NUM_FILES = 10
