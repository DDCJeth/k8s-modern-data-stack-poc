# DATA ENGINEERING POC

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

### Architecture


## Prise en main


## Details

### Structure générale du repo (A MODFIER)

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


---
