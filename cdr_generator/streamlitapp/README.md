# CDR Generator Web Application

A user-friendly Streamlit web application for generating realistic CDR (Call Detail Records) data in batch or streaming mode.

## Features

✅ **Two Generation Modes:**
- **Batch Mode**: Generate a fixed number of files quickly
- **Streaming Mode**: Generate files continuously with configurable delays

✅ **Flexible Configuration:**
- Select CDR type: Voice, SMS, Data, or All
- Customize number of files and records per file
- Adjust streaming delays (min/max)
- Real-time output monitoring

✅ **User-Friendly Interface:**
- Intuitive Streamlit web UI
- Live console output
- Progress tracking
- Configuration preview

✅ **Full Integration:**
- Uses the modular scripts from `../scripts/`
- Compatible with existing CDR generator architecture
- Easy start/stop controls

## Installation

### Prerequisites
- Python 3.7+
- Streamlit 1.28.0 or higher

### Quick Start

```bash
# Navigate to the app directory
cd streamlitapp

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Or use the provided shell script:

```bash
chmod +x run.sh
./run.sh
```

## Usage

### Batch Mode

1. Select **Batch** from the mode selector
2. Choose your CDR type (Voice, SMS, Data, or All)
3. Set the number of files to generate
4. Optionally set records per file (leave 0 for defaults)
5. Click **Start Generation**
6. Monitor the console output
7. App will auto-stop when done

**Example:** Generate 5 Voice CDR files with 2000 records each

### Streaming Mode

1. Select **Streaming** from the mode selector
2. Choose your CDR type
3. Optionally set records per file
4. Set min and max delay (in seconds) between generations
5. Click **Start Generation**
6. Files will be generated continuously
7. Monitor the console output
8. Click **Stop Generation** to halt or press Ctrl+C

**Example:** Generate SMS CDR files every 5-30 seconds with 1000 records

## Configuration Options

### Batch Mode Parameters

- **Number of files**: 1-100 (default: 5)
- **Records per file**: 100-1,000,000 (default: use type defaults)
  - Voice: 10,000 records
  - SMS: 5,000 records
  - Data: 3,000 records

### Streaming Mode Parameters

- **Records per file**: 100-1,000,000 (default: use type defaults)
- **Min delay**: 5-300 seconds (default: 10s)
- **Max delay**: 10-600 seconds (default: 120s)

## Output

All generated files are saved in the `cdr_data/` directory at the project root:

```
cdr_data/
├── cell_towers_mali.csv          # Cellular tower data
├── voice_cdr_mali_01.csv         # Voice CDR files
├── voice_cdr_mali_02.csv
├── ...
├── sms_cdr_mali_01.csv           # SMS CDR files
├── sms_cdr_mali_02.csv
├── ...
├── data_cdr_mali_01.csv          # Data CDR files
├── data_cdr_mali_02.csv
└── ...
```

## File Structure

```
streamlitapp/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── run.sh             # Shell script to run the app
└── README.md          # This file
```

## Scripts Used

The app uses the following scripts from `../scripts/`:

- **`generate_cdr.py`**: Batch mode generator
- **`streaming_generate_cdr.py`**: Streaming mode generator
- **`config.py`**: Configuration and constants
- **`generators.py`**: CDR generation functions
- **`utils.py`**: Utility functions
- **`cli.py`**: Command-line argument parsing

## Tips & Best Practices

### For Batch Mode
- Use for creating demo datasets
- Set appropriate file counts for your testing needs
- Good for batch processing and integration tests
- Generates files quickly and predictably

### For Streaming Mode
- Use for testing streaming pipelines
- Keep delays realistic (10-120 seconds recommended)
- Good for continuous integration scenarios
- Monitor output for data quality
- Use Ctrl+C or Stop button to halt

### Data Volume
- Start with smaller record counts to test
- Gradually increase for performance testing
- Consider disk space for large batches
- Monitor system resources during generation

## Troubleshooting

### Streamlit not found
```bash
pip install streamlit>=1.28.0
```

### Port already in use
Streamlit uses port 8501 by default. To use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Process not stopping
Click the **Stop Generation** button or press Ctrl+C in the terminal running Streamlit.

### Scripts not found
Ensure you're running from the `streamlitapp/` directory and that the `../scripts/` directory exists with all required Python files.

## Performance Notes

- **Batch Mode**: Can generate 100,000+ records in seconds
- **Streaming Mode**: Adjustable for different simulation speeds
- **Memory**: Efficient streaming design minimizes memory usage
- **Disk I/O**: Output written to CSV files in real-time

## Version History

**v1.0** (January 2026)
- Initial release
- Batch and streaming modes
- Real-time monitoring
- Web UI with Streamlit

## License

Part of the Orange Mali RFP Demo project

## Support

For issues or questions, refer to the main project README or contact the development team.
