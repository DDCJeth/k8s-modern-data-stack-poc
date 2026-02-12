"""
Utilitaires pour le générateur de CDR
"""

import csv
from pathlib import Path
import os

# Third-party imports for storage
try:
    import boto3
    from botocore.exceptions import NoCredentialsError
except ImportError:
    boto3 = None

try:
    import paramiko
except ImportError:
    paramiko = None


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


def upload_to_s3(local_file, bucket, s3_name=None):
    """Upload un fichier vers un bucket AWS S3"""
    if boto3 is None:
        print("Erreur: 'boto3' n'est pas installé. Impossible d'utiliser S3.")
        return False

    if s3_name is None:
        s3_name = os.path.basename(local_file)

    s3 = boto3.client('s3')
    try:
        s3.upload_file(str(local_file), bucket, s3_name)
        print(f"  [S3] Upload réussi: s3://{bucket}/{s3_name}")
        return True
    except FileNotFoundError:
        print("  [S3] Erreur: Le fichier n'a pas été trouvé.")
        return False
    except NoCredentialsError:
        print("  [S3] Erreur: Credentials AWS non trouvés.")
        return False
    except Exception as e:
        print(f"  [S3] Erreur: {e}")
        return False


def upload_to_sftp(local_file, host, username, password, remote_path='/', port=22):
    """Upload un fichier vers un serveur SFTP"""
    if paramiko is None:
        print("Erreur: 'paramiko' n'est pas installé. Impossible d'utiliser SFTP.")
        return False

    try:
        transport = paramiko.Transport((host, int(port)))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        filename = os.path.basename(local_file)
        remote_file = os.path.join(remote_path, filename).replace('\\', '/')
        
        sftp.put(str(local_file), remote_file)
        sftp.close()
        transport.close()
        print(f"  [SFTP] Upload réussi: {host}:{remote_file}")
        return True
    except Exception as e:
        print(f"  [SFTP] Erreur: {e}")
        return False


def handle_storage(file_path, args):
    """Gère le stockage en fonction des arguments fournis"""
    # 1. Le fichier est déjà sauvegardé localement par utils.save_to_csv
    
    # 2. Gestion S3
    if args.storage == 's3':
        if not args.bucket:
            print("  [Erreur] Argument --bucket requis pour le stockage S3")
            return
        upload_to_s3(file_path, args.bucket)

    # 3. Gestion SFTP
    elif args.storage == 'sftp':
        if not all([args.sftp_host, args.sftp_user, args.sftp_password]):
            print("  [Erreur] Arguments --sftp-host, --sftp-user et --sftp-password requis")
            return
        # Utiliser le port et le chemin par défaut si non fournis
        port = args.sftp_port if hasattr(args, 'sftp_port') and args.sftp_port else 22
        path = args.sftp_path if hasattr(args, 'sftp_path') and args.sftp_path else '/'
        
        upload_to_sftp(
            file_path, 
            args.sftp_host, 
            args.sftp_user, 
            args.sftp_password, 
            path,
            port
        )