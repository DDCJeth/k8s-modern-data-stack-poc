# Installation & Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Git (optional, for cloning)

## Installation Steps

### 1. Clone or Download the Project

```bash
# Using git
git clone <repository-url>
cd Poc_rfp_omea

# Or download and extract the ZIP file
cd Poc_rfp_omea
```

### 2. Install Base Requirements (Optional)

The scripts use only Python standard library, so no installation needed for batch/streaming modes.

```bash
# Optional: Install any Python standard library dependencies
python3 -m pip install --upgrade pip
```

### 3. Setup Streamlit Web Application (Recommended)

```bash
# Navigate to streamlit app directory
cd streamlitapp

# Install Streamlit and dependencies
pip install -r requirements.txt

# Alternative: Install directly
pip install streamlit>=1.28.0
```

### 4. Verify Installation

```bash
# Check Python version
python3 --version

# Check Streamlit installation
streamlit --version

# Check if scripts folder exists
ls -la ../scripts/
```

## Running the Application

### Option 1: Web Interface (Recommended for Users)

```bash
# Method 1: Using shell script
cd streamlitapp
chmod +x run.sh
./run.sh

# Method 2: Direct Streamlit command
cd streamlitapp
streamlit run app.py

# Method 3: Custom port (if 8501 is busy)
cd streamlitapp
streamlit run app.py --server.port 8502
```

**Access the app at:**
```
http://localhost:8501
```

### Option 2: Batch Mode (Command Line)

```bash
cd scripts

# Basic usage
python3 generate_cdr.py --type voice

# With custom parameters
python3 generate_cdr.py --type all --file 5 --records 2000
```

### Option 3: Streaming Mode (Command Line)

```bash
cd scripts

# Basic usage
python3 streaming_generate_cdr.py --type voice

# With custom parameters
python3 streaming_generate_cdr.py --type all --min-delay 10 --max-delay 60

# Stop with Ctrl+C
```

## Directory Structure

```
Poc_rfp_omea/
├── scripts/                          # Python modules
│   ├── generate_cdr.py              # Batch mode entry point
│   ├── streaming_generate_cdr.py     # Streaming mode entry point
│   ├── config.py                    # Configuration
│   ├── generators.py                # CDR generators
│   ├── utils.py                     # Utilities
│   └── cli.py                       # Command-line interface
├── streamlitapp/                     # Web application
│   ├── app.py                       # Main Streamlit app
│   ├── requirements.txt             # Dependencies
│   ├── run.sh                       # Launch script
│   ├── README.md                    # App documentation
│   └── .streamlit/
│       └── config.toml              # Streamlit config
├── cdr_data/                        # Output directory (auto-created)
├── README.md                        # Main documentation
├── QUICKSTART.md                    # Quick start guide
└── requirements.txt                 # Project dependencies
```

## Common Issues & Solutions

### Issue: "streamlit: command not found"

**Solution:**
```bash
pip install streamlit>=1.28.0
# Or upgrade pip first
python3 -m pip install --upgrade pip
pip install streamlit>=1.28.0
```

### Issue: Port 8501 already in use

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Or find and kill the process
lsof -ti:8501 | xargs kill -9
```

### Issue: Permission denied on run.sh

**Solution:**
```bash
chmod +x streamlitapp/run.sh
./streamlitapp/run.sh
```

### Issue: "No module named scripts"

**Solution:**
```bash
# Make sure you're in the correct directory
cd Poc_rfp_omea

# Or run from scripts directory
cd scripts
python3 generate_cdr.py --type voice
```

### Issue: No files generated in cdr_data/

**Solution:**
```bash
# Create the directory manually if needed
mkdir -p cdr_data

# Check write permissions
ls -la cdr_data/

# Try running with explicit path
python3 scripts/generate_cdr.py --type voice --file 1
```

### Issue: App freezes or slow output

**Solution:**
```bash
# Reduce the number of records
python3 scripts/generate_cdr.py --type voice --file 1 --records 100

# Or use streaming with longer delays
python3 scripts/streaming_generate_cdr.py --type voice --min-delay 30 --max-delay 60
```

## Environment Setup

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r streamlitapp/requirements.txt

# Run the app
cd streamlitapp
streamlit run app.py
```

### Using Conda (Alternative)

```bash
# Create conda environment
conda create -n cdr-generator python=3.9

# Activate
conda activate cdr-generator

# Install dependencies
pip install -r streamlitapp/requirements.txt

# Run the app
cd streamlitapp
streamlit run app.py
```

## Configuration

### Streamlit Configuration

Edit `streamlitapp/.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#FF6B35"          # Change theme colors
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#E8E8E8"
textColor = "#262730"

[server]
maxUploadSize = 200               # Max file upload size in MB
enableCORS = false               # CORS settings
enableXsrfProtection = true      # Security

[client]
showErrorDetails = true           # Show detailed error messages
```

### Python Configuration

Edit `scripts/config.py` for data generation settings:
- Cell tower definitions
- CDR types and amounts
- Tarification rates
- Field definitions

## Verification

### Check Installation

```bash
# Verify Python
python3 --version

# Verify Streamlit
streamlit --version

# Verify scripts exist
ls -la scripts/*.py

# Test batch mode
cd scripts
python3 generate_cdr.py --type voice --file 1 --records 100

# Check output
ls -la ../cdr_data/
```

### Test Data Generation

```bash
# Quick test (should complete in seconds)
cd scripts
python3 generate_cdr.py --type voice --file 1 --records 100

# Verify output
head -5 ../cdr_data/voice_cdr_mali_01.csv
```

## First Run Checklist

- [ ] Python 3.7+ installed
- [ ] Project folder extracted/cloned
- [ ] Streamlit installed (`pip install streamlit`)
- [ ] Navigated to correct directory
- [ ] Test batch mode works
- [ ] Streamlit app launches successfully
- [ ] Can generate files from web interface
- [ ] Output files created in `cdr_data/`

## Performance Recommendations

### For Batch Mode
- Start with small numbers: `--file 1 --records 100`
- Gradually increase to test system capacity
- Typical: 10k records per second on modern hardware

### For Streaming Mode
- Recommended delays: 10-120 seconds
- Start with 5 files before continuous generation
- Monitor system resources (CPU, disk I/O)

### For Web Interface
- Keep records per file ≤ 50,000 for responsive UI
- Use file browser or terminal to check large batches
- Monitor Chrome DevTools for performance issues

## Troubleshooting Checklist

1. ✅ Is Python 3.7+ installed? `python3 --version`
2. ✅ Is Streamlit installed? `pip show streamlit`
3. ✅ Are scripts in `scripts/` directory?
4. ✅ Can you run batch mode directly?
5. ✅ Does `cdr_data/` directory exist or get created?
6. ✅ Do you have write permissions in the project folder?
7. ✅ Is the correct port available (8501 default)?

## Getting Help

### Documentation Files
- `README.md` - Complete project documentation
- `QUICKSTART.md` - Quick start examples
- `streamlitapp/README.md` - Web app documentation
- `STREAMLIT_APP_SUMMARY.md` - Technical details

### Common Commands Reference

```bash
# Batch mode
python3 scripts/generate_cdr.py --type voice --file 5

# Streaming mode
python3 scripts/streaming_generate_cdr.py --type all

# Web interface
cd streamlitapp && streamlit run app.py

# Check files
ls -lh cdr_data/

# Count records
wc -l cdr_data/*.csv
```

## Next Steps

1. ✅ Complete installation
2. ✅ Run a quick test
3. 📖 Read QUICKSTART.md for usage examples
4. 🖥️ Launch web interface
5. 📊 Generate sample data
6. 🔄 Integrate with your platform
7. 📈 Analyze and visualize results

---

**Installation Complete!** 🎉

You're ready to generate CDR data. Start with:
```bash
cd streamlitapp && streamlit run app.py
```

Enjoy! 🚀
