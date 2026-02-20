# Guide de Démarrage Rapide

## 🚀 3 Façons d'Utiliser le Générateur CDR

### 1. 🖥️ Interface Web (Recommandé pour débutants)

**Avantages:** Ergonomique, facile à utiliser, monitoring en temps réel

```bash
cd streamlitapp
pip install -r requirements.txt
streamlit run app.py
```

Puis ouvrez votre navigateur à `http://localhost:8501`

**Étapes:**
1. Sélectionnez le mode (Batch ou Streaming)
2. Choisissez le type de CDR (Voice, SMS, Data, All)
3. Configurez les paramètres
4. Cliquez "Start Generation"
5. Surveillez la sortie console

---

### 2. Script (Manuellement)

#### 1. 💻 Mode Batch (Rapide et Prédictible)

**Avantages:** Rapide, idéal pour les démos, généraux définis

```bash
cd scripts

# Générer 10 fichiers Voice CDR (par défaut)
python3 batch_generation_cdr.py --type voice

# Générer 5 fichiers SMS avec 2000 enregistrements chacun
python3 batch_generation_cdr.py --type sms --file 5 --records 2000

# Générer tous les types (10 fichiers par défaut)
python3 batch_generation_cdr.py --type all
```

**Exemples courants:**

| Cas d'usage | Commande |
|---|---|
| Demo rapide (1-5 min) | `python3 batch_generation_cdr.py --type voice --file 3 --records 1000` |
| Dataset complet | `python3 batch_generation_cdr.py --type all --file 10` |
| Petit test | `python3 batch_generation_cdr.py --type data --file 1 --records 500` |
| Gros volume | `python3 batch_generation_cdr.py --type all --file 20 --records 50000` |

---

#### 2. 🔄 Mode Streaming (Continu et Réaliste)

**Avantages:** Simule le trafic réel, idéal pour les tests streaming

```bash
cd scripts

# Générer Voice CDR toutes les 10-120 secondes
python3 streaming_generate_cdr.py --type voice

# Générer SMS toutes les 5-30 secondes avec 1000 records
python3 streaming_generate_cdr.py --type sms --min-delay 5 --max-delay 30 --records 1000

# Tous les types aléatoirement toutes les 20-60 secondes
python3 streaming_generate_cdr.py --type all --min-delay 20 --max-delay 60

# Arrêter: Ctrl+C
```

**Arrêt du processus:**
```bash
# Dans le terminal: Ctrl+C
# Ou tuez le processus
pkill -f streaming_generate_cdr.py
```

---

## 📊 Résultats Attendus

Les fichiers sont générés dans le répertoire `cdr_data/`:

```
cdr_data/
├── cell_towers_mali.csv      # 10 tours cellulaires (généré une fois)
├── voice_cdr_mali_01.csv     # Fichiers Voice
├── voice_cdr_mali_02.csv
├── sms_cdr_mali_01.csv       # Fichiers SMS
├── data_cdr_mali_01.csv      # Fichiers Data
└── ...
```

### Vérifier les fichiers générés:

```bash
# Lister les fichiers
ls -lh cdr_data/

# Voir les premières lignes d'un fichier
head cdr_data/voice_cdr_mali_01.csv

# Compter les lignes
wc -l cdr_data/*.csv
```

---

## 🎯 Recommandations

### Pour les Démos
```bash
# Web app - Meilleure UX
cd streamlitapp && streamlit run app.py

# Ou batch - Rapide
python3 scripts/batch_generation_cdr.py --type all --file 5
```

### Pour les Tests
```bash
# Petit volume
python3 scripts/batch_generation_cdr.py --type voice --file 1 --records 100

# Test complet
python3 scripts/batch_generation_cdr.py --type all --file 3
```

### Pour la Production/Integration Continue
```bash
# Mode batch programmé
python3 scripts/batch_generation_cdr.py --type all --file 10

# Mode streaming continu
python3 scripts/streaming_generate_cdr.py --type all --min-delay 30 --max-delay 120
```

---

## 🔧 Dépannage

| Problème | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | `pip install streamlit>=1.28.0` |
| `Permission denied` sur run.sh | `chmod +x streamlitapp/run.sh` |
| Le port 8501 est occupé | `streamlit run app.py --server.port 8502` |
| Pas de fichiers générés | Vérifiez que `cdr_data/` existe ou est créé |
| Processus streaming ne s'arrête pas | Utilisez `Ctrl+C` ou fermez la fenêtre |

---

## 📚 Documentation Complète

- **[README.md](README.md)** - Documentation complète du projet
- **[streamlitapp/README.md](streamlitapp/README.md)** - Documentation de l'app web
- **scripts/** - Code source des générateurs

---