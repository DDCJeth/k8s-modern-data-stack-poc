"""
Interface de ligne de commande pour le générateur de CDR
"""

import argparse


def parse_arguments():
    """Parse les arguments de la ligne de commande"""
    parser = argparse.ArgumentParser(
        description='Générateur de données CDRs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemples d'utilisation (Mode batch):
  python generate_cdr.py --type voice --file 5 --records 1000
  python generate_cdr.py --type sms --file 3 --records 2000
  python generate_cdr.py --type data --file 10 --records 500
  python generate_cdr.py --type all --file 10 --records 1000

Exemples d'utilisation (Mode streaming):
  python streaming_generate_cdr.py --type voice --records 1000
  python streaming_generate_cdr.py --type sms --min-delay 5 --max-delay 30
  python streaming_generate_cdr.py --type data --records 2000 --min-delay 10 --max-delay 60
        '''
    )
    
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
    
    return parser.parse_args()

