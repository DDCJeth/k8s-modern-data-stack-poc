# Telco - Générateur de Données CDR pour Démo RFP

## Vue d'ensemble

Ce projet génère des données CDR (Call Detail Records) synthétiques pour démontrer une architecture de data lakehouse moderne. Il produit des enregistrements réalistes de Voice, SMS et Data, couvrant les 8 régions du pays.

**3 façons d'accéder au générateur:**
- 🖥️ **Interface Web**: Application Streamlit ergonomique
- 💻 **Mode Batch**: Script Python pour génération rapide
- 🔄 **Mode Streaming**: Script Python pour trafic continu

### Objectif du Projet

Fournir des données de démonstration pour l'évaluation de plateformes Big Data capables de:
- Ingérer des données CDR en temps réel et en batch
- Traiter des charges de travail streaming et batch
- Stocker des données dans des formats de tables ouvertes (Apache Iceberg)
- Fournir des capacités d'analytics interactives et de visualisation
---

## Structure des Données

### 1. Voice CDR (voice_cdr_mali_XX.csv)

**Schéma:**
```csv
timestamp, call_id, caller_msisdn, callee_msisdn, call_type, duration_seconds,
cell_id, region, termination_reason, charging_amount
```

**Types d'Appels:**
- **MOC** (Mobile Originated Call) - Appel sortant, facturé
- **MTC** (Mobile Terminated Call) - Appel entrant, gratuit

**Raisons de Terminaison:**
- `NORMAL` - Appel terminé avec succès
- `FAILED` - Échec de connexion
- `USER_TERMINATED` - Utilisateur raccroche prématurément
- `NO_ANSWER` - Pas de réponse
- `NETWORK_ERROR` - Erreur réseau

**Tarification:** 0.5 FCFA/seconde pour les appels sortants (MOC)

**Exemple:**
```csv
2024-12-14T08:15:23,CALL_001,22370123456,22376234567,MOC,345,CELL_BAM_001,Bamako,NORMAL,172.5
```

### 2. SMS CDR (sms_cdr_mali_XX.csv)

**Schéma:**
```csv
timestamp, sms_id, sender_msisdn, receiver_msisdn, sms_type, message_length,
cell_id, region, delivery_status, charging_amount
```

**Types de SMS:**
- **MO** (Mobile Originated) - SMS sortant, facturé
- **MT** (Mobile Terminated) - SMS entrant, gratuit

**Statuts de Livraison:**
- `DELIVERED` - SMS livré avec succès
- `FAILED` - Échec de livraison
- `PENDING` - En attente de livraison

**Tarification:** 25 FCFA par SMS envoyé (MO)

**Exemple:**
```csv
2024-12-14T08:15:30,SMS_001,22370123456,22376234567,MO,45,CELL_BAM_001,Bamako,DELIVERED,25.0
```

### 3. Data Session CDR (data_cdr_mali_XX.csv)

**Schéma:**
```csv
timestamp, session_id, msisdn, apn, session_duration_seconds, bytes_uploaded,
bytes_downloaded, cell_id, region, session_end_reason, charging_amount
```

**Types d'APN:**
- `internet.mali` - Navigation web standard
- `mms.mali` - Multimédia Messaging Service
- `wap.mali` - WAP (mobile browsing legacy)

**Raisons de Fin de Session:**
- `NORMAL` - Session terminée normalement
- `USER_TERMINATED` - Utilisateur déconnecte
- `QUOTA_EXCEEDED` - Quota de données épuisé
- `NETWORK_ERROR` - Erreur réseau
- `TIMEOUT` - Timeout de session

**Tarification:** Variable selon l'APN (0.0001 - 0.0002 FCFA/KB)

**Exemple:**
```csv
2024-12-14T08:15:00,DATA_001,22370123456,internet.mali,3600,52428800,524288000,CELL_BAM_001,Bamako,NORMAL,500.0
```

### 4. Tours Cellulaires (cell_towers_mali.csv)

**Schéma:**
```csv
cell_id, region, province, latitude, longitude, technology, capacity_erlang
```

**Technologies Déployées:**
- **4G** - Zones urbaines (Bamako, Segou, Mopti)
- **3G** - Villes moyennes (Sikasso, Kayes, Tombouctou, Gao)
- **2G** - Zones reculées (Kidal)

**Exemple:**
```csv
CELL_BAM_001,Bamako,Bamako Capital,12.6392,-8.0029,4G,150
```

---

## Régions Couvertes

Le générateur crée des données pour les **8 régions administratives du Mali** :

| Région | Capitale | Technologie | Coordonnées GPS | Code Cell |
|--------|----------|-------------|-----------------|-----------|
| **Bamako** | Bamako | 4G/3G | 12.6392°N, 8.0029°W | CELL_BAM |
| **Segou** | Ségou | 4G | 13.4317°N, 6.2664°W | CELL_SEG |
| **Sikasso** | Sikasso | 3G | 11.3177°N, 5.6661°W | CELL_SIK |
| **Kayes** | Kayes | 3G | 14.4474°N, 11.4448°W | CELL_KAY |
| **Mopti** | Mopti | 4G | 14.4844°N, 4.1966°W | CELL_MOP |
| **Tombouctou** | Tombouctou | 3G | 16.7734°N, 3.0074°W | CELL_TOM |
| **Gao** | Gao | 3G | 16.2719°N, 0.0447°W | CELL_GAO |
| **Kidal** | Kidal | 2G | 18.4411°N, 1.4078°E | CELL_KID |

---

## Installation et Utilisation

### Prérequis

- Python 3.7+
- Bibliothèques standard Python (csv, random, datetime, pathlib, argparse)

### Installation

```bash
# Cloner ou télécharger le projet
cd /chemin/vers/RFP

# Aucune dépendance externe requise pour batch/streaming
# Streamlit est optionnel mais recommandé pour l'interface web
```

## 🖥️ Web Application (Streamlit)

### Accès Rapide

```bash
# Depuis le répertoire streamlitapp
cd streamlitapp
pip install -r requirements.txt
streamlit run app.py
```

Ou utilisez le script fourni:
```bash
cd streamlitapp
chmod +x run.sh
./run.sh
```

L'application sera accessible à `http://localhost:8501`

### Avantages de l'Interface Web

✅ **Ergonomique**: Interface intuitive et visuelle  
✅ **Contrôle Facile**: Paramètres facilement ajustables  
✅ **Monitoring**: Sortie console en temps réel  
✅ **Flexible**: Support batch et streaming depuis la même app  
✅ **Intégré**: Utilise les mêmes scripts que la CLI  

### Features Web App

- 📊 Mode Batch et Streaming
- 🎙️ Sélection du type de CDR (Voice, SMS, Data, All)
- ⏱️ Délais configurables pour streaming
- 🎛️ Ajustement en temps réel des paramètres
- 📈 Monitoring en direct de la génération
- ⏹️ Contrôle Start/Stop
- 📋 Aperçu de la configuration

Pour plus de détails, voir [streamlitapp/README.md](streamlitapp/README.md)


### Exécution - Mode Batch

Le script principal utilise une interface de ligne de commande avec des arguments requis et optionnels:

```bash
python generate_cdr.py --type <TYPE> [--file NUM_FILES] [--records NUM_RECORDS]
```

#### Arguments (Mode Batch):

- `--type` **(requis)** : Type de CDR à générer
  - `voice` : Générer uniquement des Voice CDR
  - `sms` : Générer uniquement des SMS CDR
  - `data` : Générer uniquement des Data CDR
  - `all` : Générer tous les types de CDR

- `--file` (optionnel) : Nombre de fichiers à générer (défaut: 10)

- `--records` (optionnel) : Nombre d'enregistrements par fichier
  - Défaut: 10,000 pour voice, 5,000 pour sms, 3,000 pour data

#### Exemples d'utilisation (Mode Batch):

```bash
# Générer uniquement 5 fichiers Voice CDR avec 1000 enregistrements chacun
python generate_cdr.py --type voice --file 5 --records 1000

# Générer 3 fichiers SMS CDR avec 2000 enregistrements chacun
python generate_cdr.py --type sms --file 3 --records 2000

# Générer tous les types de CDR avec les valeurs par défaut (10 fichiers)
python generate_cdr.py --type all

# Générer 2 fichiers Data CDR avec 5000 enregistrements chacun
python generate_cdr.py --type data --file 2 --records 5000
```

### Exécution - Mode Streaming

Le script de streaming génère les fichiers de manière continue à intervalles aléatoires jusqu'à l'arrêt de l'utilisateur (Ctrl+C):

```bash
python streaming_generate_cdr.py --type <TYPE> [--records NUM_RECORDS] [--min-delay SEC] [--max-delay SEC]
```

#### Arguments (Mode Streaming):

- `--type` **(requis)** : Type de CDR à générer
  - `voice` : Générer uniquement des Voice CDR
  - `sms` : Générer uniquement des SMS CDR
  - `data` : Générer uniquement des Data CDR
  - `all` : Générer tous les types aléatoirement

- `--records` (optionnel) : Nombre d'enregistrements par fichier
  - Défaut: 10,000 pour voice, 5,000 pour sms, 3,000 pour data

- `--min-delay` (optionnel) : Délai minimum entre les générations en secondes (défaut: 10s)

- `--max-delay` (optionnel) : Délai maximum entre les générations en secondes (défaut: 120s)

#### Exemples d'utilisation (Mode Streaming):

```bash
# Générer des Voice CDR toutes les 10-120 secondes (délai par défaut)
python streaming_generate_cdr.py --type voice

# Générer des SMS CDR toutes les 5-30 secondes avec 2000 enregistrements
python streaming_generate_cdr.py --type sms --records 2000 --min-delay 5 --max-delay 30

# Générer tous les types aléatoirement toutes les 10-60 secondes
python streaming_generate_cdr.py --type all --min-delay 10 --max-delay 60

# Générer des Data CDR toutes les 20-90 secondes
python streaming_generate_cdr.py --type data --min-delay 20 --max-delay 90

# Arrêter le processus
# Appuyer sur Ctrl+C pour arrêter le générateur et voir le résumé final
```

**Caractéristiques du Mode Streaming:**
- ✅ Génère les fichiers en continu jusqu'à l'arrêt de l'utilisateur
- ✅ Délais aléatoires entre les générations pour simuler un trafic réaliste
- ✅ Si `--type all` est spécifié, alterne aléatoirement entre les types de CDR
- ✅ Affiche les statistiques en temps réel (timestamp, compteurs, délai suivant)
- ✅ Résumé final des fichiers générés lors de l'arrêt

### Sortie

Le script génère un répertoire `cdr_data/` contenant :

```
cdr_data/
├── cell_towers_mali.csv              # 10 tours cellulaires
├── voice_cdr_mali_01.csv             # 10,000 enregistrements
├── voice_cdr_mali_02.csv             # 10,000 enregistrements
├── ...
├── voice_cdr_mali_10.csv             # 10,000 enregistrements
├── sms_cdr_mali_01.csv               # 5,000 enregistrements
├── sms_cdr_mali_02.csv               # 5,000 enregistrements
├── ...
├── sms_cdr_mali_10.csv               # 5,000 enregistrements
├── data_cdr_mali_01.csv              # 3,000 enregistrements
├── data_cdr_mali_02.csv              # 3,000 enregistrements
├── ...
└── data_cdr_mali_10.csv              # 3,000 enregistrements
```

**Volumes Totaux:**
- Voice CDR: **100,000 enregistrements** (10 fichiers × 10,000)
- SMS CDR: **50,000 enregistrements** (10 fichiers × 5,000)
- Data CDR: **30,000 enregistrements** (10 fichiers × 3,000)
- Cell Towers: **10 tours** (1 fichier)

---

## Architecture Modulaire

Le générateur CDR a été restructuré en modules spécialisés pour améliorer la maintenabilité et l'extensibilité.

### Structure générale du projet

```
Poc_rfp_omea/
├── scripts/                         # Modules Python (batch/streaming)
│   ├── generate_cdr.py             # Mode batch
│   ├── streaming_generate_cdr.py    # Mode streaming
│   ├── config.py                   # Configuration
│   ├── generators.py               # Générateurs CDR
│   ├── utils.py                    # Utilitaires
│   └── cli.py                      # Interface CLI
├── streamlitapp/                    # Application Web
│   ├── app.py                      # Application Streamlit
│   ├── requirements.txt            # Dépendances
│   ├── run.sh                      # Script de lancement
│   ├── README.md                   # Documentation
│   └── .streamlit/
│       └── config.toml             # Configuration Streamlit
├── cdr_data/                       # Répertoire de sortie (généré)
├── README.md                       # Ce fichier
└── requirements.txt                # Dépendances principales
```

### Structure des fichiers de scripts

```
scripts/
├── generate_cdr.py          # Point d'entrée principal (batch)
├── streaming_generate_cdr.py # Point d'entrée streaming
├── config.py               # Configuration et constantes
├── cli.py                  # Interface de ligne de commande
├── generators.py           # Génération des CDR (Voice, SMS, Data)
├── utils.py                # Utilitaires (CSV, répertoires)
├── README.md               # Documentation
├── streaming_generate_cdr.py # Mode streaming (temps réel)
└── cdr_data/               # Répertoire de sortie (créé automatiquement)
    ├── cell_towers_mali.csv
    ├── voice_cdr_mali_01.csv
    ├── voice_cdr_mali_02.csv
    ├── ...
    ├── sms_cdr_mali_01.csv
    ├── sms_cdr_mali_02.csv
    ├── ...
    ├── data_cdr_mali_01.csv
    ├── data_cdr_mali_02.csv
    └── ...
```

### Description des modules

#### `config.py`
Contient toutes les constantes et configurations du projet:
- Définition des régions et tours cellulaires du Mali
- Types d'appels, SMS et sessions data
- Raisons de terminaison et statuts de livraison
- Champs CSV pour chaque type de CDR
- Valeurs par défaut pour le nombre de fichiers et d'enregistrements

#### `cli.py`
Gère l'interface de ligne de commande:
- Analyse des arguments `--type`, `--file`, `--records`, `--min-delay`, et `--max-delay`
- Validation des paramètres
- Affichage de l'aide et des exemples

#### `generators.py`
Contient les fonctions de génération des CDR:
- `generate_msisdn()` : Génère des numéros de téléphone maliens
- `generate_voice_cdr()` : Génère les enregistrements d'appels
- `generate_sms_cdr()` : Génère les enregistrements de SMS
- `generate_data_cdr()` : Génère les enregistrements de sessions data

#### `utils.py`
Contient les fonctions utilitaires:
- `save_to_csv()` : Sauvegarde les enregistrements dans un fichier CSV
- `generate_cell_towers_csv()` : Génère le fichier des tours cellulaires
- `ensure_output_dir()` : Crée le répertoire de sortie

#### `generate_cdr.py`
Point d'entrée principal (mode batch) qui orchestrate tout:
- Parse les arguments de ligne de commande
- Initialise les répertoires
- Appelle les générateurs appropriés selon le type sélectionné
- Affiche un résumé des fichiers générés

#### `streaming_generate_cdr.py`
Point d'entrée pour le mode streaming qui génère les fichiers en continu:
- Parse les arguments incluant `--min-delay` et `--max-delay`
- Initialise les tours cellulaires
- Boucle infinie qui génère les fichiers à intervales aléatoires
- Affiche les statistiques en temps réel
- Capture Ctrl+C pour afficher le résumé final

### Avantages de cette architecture

✅ **Modularité** : Chaque module a une responsabilité unique  
✅ **Maintenabilité** : Facile à modifier et à debugger  
✅ **Extensibilité** : Simple d'ajouter de nouveaux types de CDR  
✅ **Réutilisabilité** : Les modules peuvent être importés et utilisés indépendamment  
✅ **Testabilité** : Chaque fonction peut être testée isolément  
✅ **Flexibilité** : Support de deux modes d'exécution (batch et streaming)

---

## Modes d'Exécution

### Mode Batch (generate_cdr.py)

Génère un nombre prédéfini de fichiers et s'arrête automatiquement.

**Cas d'usage :**
- Générer des datasets de démonstration
- Tests en batch
- Ingestion planifiée de données

### Mode Streaming (streaming_generate_cdr.py)

Génère les fichiers en continu à intervalles aléatoires jusqu'à l'arrêt de l'utilisateur.

**Cas d'usage :**
- Simulation de trafic réseau en temps réel
- Tests de pipelines de streaming
- Alimentation continue d'une plateforme Big Data
- Démonstration de capacités de streaming

---

## Comment Fonctionne le Générateur CDR

### Vue d'Ensemble

Le générateur CDR est un script Python qui crée automatiquement des données télécoms réalistes pour démontrer une plateforme Big Data. Il simule le trafic d'un réseau mobile réel à travers toutes les régions du Mali.

**Deux modes disponibles:**
- **Batch**: Génère un nombre défini de fichiers rapidement
- **Streaming**: Génère les fichiers de manière continue avec des délais réalistes

### Architecture Modulaire

Le générateur est organisé en plusieurs composants distincts:

1. **Configuration des données de base** - Définit les 8 régions du Mali, les 10 tours cellulaires avec leurs coordonnées GPS réelles, et tous les types de services
2. **Génération des numéros** - Crée des numéros de téléphone maliens valides au format international
3. **Génération des CDR Voice** - Produit les enregistrements d'appels avec leur tarification
4. **Génération des CDR SMS** - Produit les enregistrements de messages texte
5. **Génération des CDR Data** - Produit les enregistrements de sessions internet
6. **Sauvegarde en CSV** - Exporte toutes les données dans des fichiers structurés

### 1. Génération des Numéros de Téléphone

Le générateur crée des numéros MSISDN maliens conformes au standard international ITU-T E.164. Chaque numéro commence par 223 (code pays du Mali), suivi d'un préfixe mobile entre 70 et 79, puis de 6 chiffres aléatoires. Ce format produit des numéros comme 22370123456 ou 22375987654, identiques à ceux utilisés dans le réseau réel.

### 2. Configuration des Tours Cellulaires

Le générateur définit 10 tours cellulaires réparties à travers les 8 régions du Mali. Chaque tour possède des coordonnées GPS authentiques des capitales régionales, une technologie adaptée à sa zone (4G pour Bamako la capitale, 3G pour les villes moyennes, 2G pour les zones reculées comme Kidal), et une capacité de trafic mesurée en Erlangs selon les standards télécoms.

### 3. Génération des Voice CDR (Appels)

Pour chaque appel, le générateur simule un comportement réseau réaliste:

**Distribution des statuts:**
- 80% des appels se terminent normalement (NORMAL)
- Les 20% restants se répartissent entre échecs de connexion, pas de réponse, utilisateur raccroche, et erreurs réseau

**Calcul de la durée:**
- Les appels réussis durent entre 30 secondes et 30 minutes
- Les appels interrompus par l'utilisateur durent entre 10 secondes et 5 minutes
- Les appels échoués ont une durée de 0 seconde

**Tarification:**
- Les appels sortants (MOC) sont facturés à 0,5 FCFA par seconde
- Les appels entrants (MTC) sont gratuits pour le receveur
- Les appels échoués ne sont pas facturés

**Progression temporelle:**
- Les appels sont espacés de 1 à 30 secondes pour simuler un trafic réaliste

### 4. Génération des SMS CDR

Le générateur crée des enregistrements SMS avec ces caractéristiques:

**Distribution des statuts:**
- 90% des SMS sont livrés avec succès (taux plus élevé que les appels car moins de ressources réseau nécessaires)
- 5% échouent et 5% sont en attente

**Longueur des messages:**
- Chaque SMS a une longueur aléatoire entre 10 et 160 caractères (limite standard GSM)

**Tarification:**
- Les SMS sortants (MO) coûtent 25 FCFA de manière forfaitaire
- Les SMS entrants (MT) sont gratuits
- Les SMS non livrés ne sont pas facturés

**Progression temporelle:**
- Les SMS sont espacés de 1 à 20 secondes (plus fréquents que les appels)

### 5. Génération des Data CDR (Sessions Internet)

Le générateur simule trois types de sessions data selon l'APN utilisé:

**Internet.mali (Navigation web standard):**
- Volumes d'upload: 1 MB à 100 MB
- Volumes de download: 10 MB à 1 GB (ratio 1:10 réaliste)
- Tarif: 0,0002 FCFA par KB

**MMS.mali (Multimédia Messaging):**
- Volumes d'upload: 512 KB à 10 MB (envoi de photos)
- Volumes de download: 1 MB à 20 MB
- Tarif: 0,0001 FCFA par KB

**WAP.mali (Mobile browsing legacy):**
- Volumes d'upload: 512 KB à 5 MB
- Volumes de download: 2 MB à 50 MB
- Tarif: 0,00015 FCFA par KB

**Distribution des statuts:**
- 85% des sessions se terminent normalement
- Les autres cas incluent déconnexion utilisateur, quota épuisé, erreur réseau, ou timeout

**Calcul de tarification:**
- Le montant facturé est calculé sur le volume total (upload + download)
- Conversion en kilobytes puis application du tarif selon l'APN
- Seules les sessions normales sont facturées

**Progression temporelle:**
- Les sessions sont espacées de 30 secondes à 3 minutes (moins fréquentes mais plus longues)

### 6. Organisation en Fichiers Multiples

Le générateur produit 31 fichiers CSV organisés de manière stratégique:

**Voice CDR:**
- 10 fichiers de 10 000 enregistrements chacun
- Nommés voice_cdr_mali_01.csv à voice_cdr_mali_10.csv
- Représente 100 000 appels au total

**SMS CDR:**
- 10 fichiers de 5 000 enregistrements chacun
- Nommés sms_cdr_mali_01.csv à sms_cdr_mali_10.csv
- Représente 50 000 SMS au total

**Data CDR:**
- 10 fichiers de 3 000 enregistrements chacun
- Nommés data_cdr_mali_01.csv à data_cdr_mali_10.csv
- Représente 30 000 sessions data au total

**Cell Towers:**
- 1 fichier de référence avec 10 tours
- Nommé cell_towers_mali.csv

**Décalage temporel:**
Chaque fichier représente une heure de trafic. Le premier fichier commence le 14 décembre 2024 à 8h00, le deuxième à 9h00, et ainsi de suite. Cette organisation simule l'arrivée périodique de CDR comme dans un réseau réel où les données sont collectées par batch horaires.

### 7. Distribution Géographique

Chaque enregistrement CDR est associé aléatoirement à l'une des 10 tours cellulaires, ce qui distribue le trafic à travers toutes les régions du Mali:

- Bamako (capitale) dispose de 3 tours en 4G et 3G
- Segou, Sikasso, Kayes, Mopti, Tombouctou, Gao ont chacune 1 tour
- Kidal (zone reculée) a une tour 2G avec faible capacité

Cette distribution reflète la couverture réseau réelle où les zones urbaines ont plus d'infrastructure que les zones rurales.


### 8. Processus d'Exécution

Lorsque le script est lancé, il exécute ces étapes dans l'ordre:

1. Crée un répertoire de sortie appelé "cdr_data"
2. Génère d'abord le fichier de référence des tours cellulaires
3. Génère les 10 fichiers Voice CDR avec progression horaire
4. Génère les 10 fichiers SMS CDR avec progression horaire
5. Génère les 10 fichiers Data CDR avec progression horaire
6. Affiche un résumé avec les totaux et l'emplacement des fichiers

Le processus complet prend quelques minutes selon la puissance de la machine.

### 9. Format de Sortie CSV

Tous les fichiers sont exportés en format CSV (Comma-Separated Values) avec:

- Une ligne d'en-tête contenant les noms des colonnes
- Un encodage UTF-8 pour supporter les caractères spéciaux des noms de régions
- Des virgules comme séparateurs de champs
- Des timestamps au format ISO 8601 (YYYY-MM-DDTHH:MM:SS)

Ce format est compatible avec tous les outils d'ingestion Big Data (NiFi, Kafka, Spark) et peut être facilement importé dans des bases de données ou des outils d'analyse.

### Principes de Conception

**Modularité:**
Le générateur est divisé en fonctions spécialisées, chacune responsable d'une seule tâche. Cela facilite la maintenance et les modifications futures.

**Réutilisabilité:**
Les fonctions communes (comme la sauvegarde CSV) sont utilisées pour tous les types de données, évitant la duplication de code.

**Extensibilité:**
Il est facile d'ajouter de nouvelles régions, modifier les volumes de données, ou créer de nouveaux types de CDR sans restructurer le code.

**Conformité aux standards:**
Le générateur respecte les normes de l'industrie télécoms (3GPP pour les CDR, ITU-T pour la numérotation, ETSI pour les standards européens).

### Logique de Tarification Globale

**Voice:** Les appels sortants sont facturés à la seconde (0,5 FCFA/sec), les appels entrants sont gratuits, et les échecs ne sont jamais facturés.

**SMS:** Tarification forfaitaire de 25 FCFA par SMS envoyé avec succès, gratuit pour les SMS reçus et non facturé en cas d'échec.

**Data:** Tarification au volume selon le type de service (internet, MMS, ou WAP), calculée sur le total des octets transférés et facturée uniquement pour les sessions terminées normalement.

---

## Licence et Contact

**Projet:**  RFP Demo - Générateur CDR
**Version:** 1.0
**Date:** Décembre 2024
**Contact:**  - Direction Technique

---
