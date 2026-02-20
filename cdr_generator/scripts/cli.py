"""
Interface de ligne de commande pour le générateur de CDR
Mise à jour : Support pour les arguments de stockage (S3, MinIO et SFTP)
"""

import argparse


def parse_arguments():
    """Parse les arguments de la ligne de commande"""
    parser = argparse.ArgumentParser(
        description='Générateur de données CDRs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemples d'utilisation (Mode batch local):
  python batch_generation_cdr.py --type voice --file 5 --records 1000

Exemples d'utilisation (Stockage AWS S3 standard):
  python batch_generation_cdr.py --type sms --storage s3 --bucket mon-bucket-aws

Exemples d'utilisation (Stockage MinIO S3):
  python batch_generation_cdr.py --type data --storage s3 --bucket mon-bucket-minio --endpoint-url http://127.0.0.1:9000 --access-key minioadmin --secret-key minioadmin

Exemples d'utilisation (Stockage SFTP):
  python batch_generation_cdr.py --type data --storage sftp --sftp-host 192.168.1.50 --sftp-user user --sftp-password pass --sftp-path /
        '''
    )
    
    # --- Arguments existants ---
    parser.add_argument(
        '--type',
        choices=['voice', 'sms', 'data', 'all'],
        required=True,
        help='Type de CDR à générer: voice, sms, data ou all (requis)'
    )
    
    parser.add_argument(
        '--file',
        type=int,
        default=10,
        help='Nombre de fichiers à générer en batch (défaut: 10)'
    )
    
    parser.add_argument(
        '--records',
        type=int,
        default=None,
        help='Nombre d\'enregistrements par fichier (défaut: 10000 pour voice, 5000 pour sms, 3000 pour data)'
    )
    
    parser.add_argument(
        '--min-delay',
        type=int,
        default=10,
        help='Délai minimum entre les générations en mode streaming en secondes (défaut: 10)'
    )
    
    parser.add_argument(
        '--max-delay',
        type=int,
        default=120,
        help='Délai maximum entre les générations en mode streaming en secondes (défaut: 120)'
    )

    # --- Nouveaux arguments pour la gestion de l'état ---
    state_group = parser.add_argument_group('Options d\'état (State)')
    
    state_group.add_argument(
        '--reset-state',
        action='store_true',
        help='Force la réinitialisation de l\'état (ignore et écrase le fichier state_generation.txt existant)'
    )

    # --- Nouveaux arguments pour le stockage ---
    storage_group = parser.add_argument_group('Options de stockage')

    storage_group.add_argument(
        '--storage',
        choices=['local', 's3', 'sftp'],
        default='local',
        help='Destination du stockage des fichiers (défaut: local)'
    )

    # Arguments S3 et MinIO
    s3_group = parser.add_argument_group('Options S3 / MinIO (requis si --storage s3)')
    s3_group.add_argument(
        '--bucket',
        type=str,
        help='Nom du bucket AWS S3 ou MinIO'
    )
    s3_group.add_argument(
        '--endpoint-url',
        type=str,
        help='URL du endpoint MinIO (ex: http://127.0.0.1:9000)'
    )
    s3_group.add_argument(
        '--access-key',
        type=str,
        help='Access Key ID pour MinIO ou S3 Custom'
    )
    s3_group.add_argument(
        '--secret-key',
        type=str,
        help='Secret Access Key pour MinIO ou S3 Custom'
    )

    # Arguments SFTP
    sftp_group = parser.add_argument_group('Options SFTP (requis si --storage sftp)')
    sftp_group.add_argument(
        '--sftp-host',
        type=str,
        help='Adresse hôte du serveur SFTP'
    )
    sftp_group.add_argument(
        '--sftp-user',
        type=str,
        help='Nom d\'utilisateur SFTP'
    )
    sftp_group.add_argument(
        '--sftp-password',
        type=str,
        help='Mot de passe SFTP'
    )
    sftp_group.add_argument(
        '--sftp-port',
        type=int,
        default=22,
        help='Port SFTP (défaut: 22)'
    )
    sftp_group.add_argument(
        '--sftp-path',
        type=str,
        default='/',
        help='Chemin du répertoire distant sur le serveur SFTP (défaut: /)'
    )
    
    return parser.parse_args()