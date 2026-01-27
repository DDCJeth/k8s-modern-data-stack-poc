# Orange Mali - Générateur de Données CDR pour Démo RFP

## Vue d'ensemble

Ce projet génère des données CDR (Call Detail Records) synthétiques pour démontrer une architecture de data lakehouse moderne pour Orange Mali. Il produit des enregistrements réalistes de Voice, SMS et Data, couvrant les 8 régions du Mali.

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
- Bibliothèques standard Python (csv, random, datetime, pathlib)

### Installation

```bash
# Cloner ou télécharger le projet
cd /chemin/vers/RFP

# Aucune dépendance externe requise
# Le script utilise uniquement des modules Python standard
```

### Exécution

```bash
python generate_cdr_data.py
```

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

## Comment Fonctionne le Générateur CDR

### Vue d'Ensemble

Le générateur CDR est un script Python qui crée automatiquement des données télécoms réalistes pour démontrer une plateforme Big Data. Il simule le trafic d'un réseau mobile réel sur 10 heures d'activité à travers toutes les régions du Mali.

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

**Projet:** Orange Mali RFP Demo - Générateur CDR
**Version:** 1.0
**Date:** Décembre 2024
**Contact:** Orange Mali - Direction Technique

---
