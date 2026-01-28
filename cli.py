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
Exemples d'utilisation:
  python generate_cdr.py --type voice --file 5 --records 1000
  python generate_cdr.py --type sms --file 3 --records 2000
  python generate_cdr.py --type data --file 10 --records 500
  python generate_cdr.py --type all --file 10 --records 1000
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
        help='Nombre de fichiers à générer (défaut: 10)'
    )
    
    parser.add_argument(
        '--records',
        type=int,
        default=None,
        help='Nombre d\'enregistrements par fichier (défaut: 10000 pour voice, 5000 pour sms, 3000 pour data)'
    )
    
    return parser.parse_args()
