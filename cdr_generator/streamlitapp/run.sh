#!/bin/bash
# Script to run the Streamlit CDR Generator app

cd "$(dirname "$0")"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed. Installing..."
    pip install streamlit>=1.28.0
fi

# Run the Streamlit app
streamlit run app.py --logger.level=info
