"""
CDR Generator Web Application
Streamlit app for generating CDR data in batch or streaming mode
"""

import streamlit as st
import subprocess
import time
from datetime import datetime
from pathlib import Path
import sys

# Add scripts folder to path
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

# Page configuration
st.set_page_config(
    page_title="CDR Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.title("📊 CDR Data Generator")
st.markdown("Generate realistic Call Detail Records (Voice, SMS, Data) for demonstration and testing")

# Initialize session state
if 'generation_active' not in st.session_state:
    st.session_state.generation_active = False
if 'generation_process' not in st.session_state:
    st.session_state.generation_process = None

# Main layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### ⚙️ Configuration")
    
    # Mode selection
    mode = st.radio(
        "**Generation Mode**",
        options=["Batch", "Continuous"],
        help="""Batch: Generates a defined number of files. Continuous: Generates files continuously with random generation times."""
    )
    
    # CDR Type selection
    cdr_type = st.selectbox(
        "**CDR Type**",
        options=["voice", "sms", "data", "all"],
        format_func=lambda x: {
            "voice": "🎙️ Voice Calls",
            "sms": "💬 SMS Messages",
            "data": "📡 Data Sessions",
            "all": "🔄 All Types"
        }[x]
    )
    
    st.markdown("---")
    
    # Mode-specific settings
    if mode == "Batch":
        st.markdown("### 📋 Batch Settings")
        
        num_files = st.number_input(
            "Number of files to generate",
            min_value=1,
            max_value=100,
            value=5,
            step=1,
            help="Number of CSV files to generate"
        )
        
        num_records = st.number_input(
            "Records per file (optional)",
            min_value=100,
            max_value=1000000,
            value=100,
            step=100,
            help="Leave 0 to use defaults (10k voice, 5k SMS, 3k data)"
        )
        
        records_arg = f" --records {num_records}" if num_records > 0 else ""
        
    else:  # Streaming
        st.markdown("### ⏱️ Continuous Settings")
        
        num_records = st.number_input(
            "Records per file (optional)",
            min_value=100,
            max_value=1000000,
            value=100,
            step=100,
            help="Leave 100 to use defaults"
        )
        
        col_min, col_max = st.columns(2)
        with col_min:
            min_delay = st.number_input(
                "Min delay (seconds)",
                min_value=5,
                max_value=300,
                value=10,
                step=5,
                help="Minimum delay between generations"
            )
        
        with col_max:
            max_delay = st.number_input(
                "Max delay (seconds)",
                min_value=10,
                max_value=600,
                value=120,
                step=10,
                help="Maximum delay between generations"
            )
        
        if min_delay >= max_delay:
            st.error("⚠️ Min delay must be less than max delay!")
        
        records_arg = f" --records {num_records}" if num_records > 0 else ""

with col2:
    st.markdown("### 📊 Output Preview")
    
with col2:
    if cdr_type == "data":
        st.info("""
        **Data Sample**
        ```csv
        timestamp,session_id,msisdn,apn,session_duration_seconds,bytes_uploaded,bytes_downloaded,cell_id,region,session_end_reason,charging_amount
        2024-12-14T08:15:00,DATA_001,22370123456,internet.mali,3600,52428800,524288000,CELL_BAM_001,Bamako,NORMAL,500.0
        2024-12-14T08:20:00,DATA_002,22375987654,internet.mali,1800,10485760,104857600,CELL_BAM_002,Bamako,NORMAL,250.0
        ```
        """)

    elif cdr_type == "sms":
        st.info("""
        **SMS Sample**
        ```csv
        timestamp,sms_id,sender_msisdn,receiver_msisdn,sms_type,message_length,cell_id,region,delivery_status,charging_amount
        2024-12-14T08:15:30,SMS_001,22370123456,22376234567,MO,45,CELL_BAM_001,Bamako,DELIVERED,25.0
        2024-12-14T08:16:15,SMS_002,22375987654,22370456789,MO,128,CELL_BAM_002,Bamako,DELIVERED,25.0
        ```
        """)

    elif cdr_type == "voice":
        st.info("""
        **Voice Sample**
        ```csv
        timestamp,call_id,caller_msisdn,callee_msisdn,call_type,duration_seconds,cell_id,region,termination_reason,charging_amount
        2024-12-14T08:15:23,CALL_001,22370123456,22376234567,MOC,345,CELL_BAM_001,Bamako,NORMAL,172.5
        2024-12-14T08:16:45,CALL_002,22375987654,22370456789,MOC,128,CELL_BAM_002,Bamako,NORMAL,64.0
        ```
        """)

    else:
        st.info("""
        **Data Sample**
        ```csv
        timestamp,session_id,msisdn,apn,session_duration_seconds,bytes_uploaded,bytes_downloaded,cell_id,region,session_end_reason,charging_amount
        2024-12-14T08:15:00,DATA_001,22370123456,internet.mali,3600,52428800,524288000,CELL_BAM_001,Bamako,NORMAL,500.0
        2024-12-14T08:20:00,DATA_002,22375987654,internet.mali,1800,10485760,104857600,CELL_BAM_002,Bamako,NORMAL,250.0
        ```
        
        **SMS Sample**
        ```csv
        timestamp,sms_id,sender_msisdn,receiver_msisdn,sms_type,message_length,cell_id,region,delivery_status,charging_amount
        2024-12-14T08:15:30,SMS_001,22370123456,22376234567,MO,45,CELL_BAM_001,Bamako,DELIVERED,25.0
        2024-12-14T08:16:15,SMS_002,22375987654,22370456789,MO,128,CELL_BAM_002,Bamako,DELIVERED,25.0
        ```

        **Voice Sample**
        ```csv
        timestamp,call_id,caller_msisdn,callee_msisdn,call_type,duration_seconds,cell_id,region,termination_reason,charging_amount
        2024-12-14T08:15:23,CALL_001,22370123456,22376234567,MOC,345,CELL_BAM_001,Bamako,NORMAL,172.5
        2024-12-14T08:16:45,CALL_002,22375987654,22370456789,MOC,128,CELL_BAM_002,Bamako,NORMAL,64.0
        ```
        """)


    # Statistics area
    st.markdown("---")
    # st.markdown("### 📈 Generation Statistics")
    
    # stats_col1, stats_col2, stats_col3 = st.columns(3)
    # with stats_col1:
    #     st.metric("Mode", "Batch" if mode == "Batch" else "Streaming")
    # with stats_col2:
    #     st.metric("CDR Type", cdr_type.upper())
    # with stats_col3:
    #     st.metric("Status", "Ready" if not st.session_state.generation_active else "Running")

# Separator
st.markdown("---")

# Control buttons
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("▶️ Start Generation", key="start_btn", use_container_width=True):
        if mode == "Streaming" and min_delay >= max_delay:
            st.error("Invalid delay configuration!")
        else:
            st.session_state.generation_active = True
            st.rerun()

with col2:
    if st.button("⏹️ Stop Generation", key="stop_btn", use_container_width=True, disabled=not st.session_state.generation_active):
        st.session_state.generation_active = False
        if st.session_state.generation_process:
            try:
                st.session_state.generation_process.terminate()
            except:
                pass
        st.rerun()

# Generate command and execute
if st.session_state.generation_active:
    st.markdown("---")
    st.markdown("### 🚀 Running Generation")
    
    # Build command
    if mode == "Batch":
        script_name = "bash_generate_cdr.py"
        cmd = [
            "python3",
            str(scripts_path / script_name),
            "--type", cdr_type,
            "--file", str(num_files)
        ]
        if num_records > 0:
            cmd.extend(["--records", str(num_records)])
    else:
        script_name = "streaming_generate_cdr.py"
        cmd = [
            "python3",
            str(scripts_path / script_name),
            "--type", cdr_type,
            "--min-delay", str(min_delay),
            "--max-delay", str(max_delay)
        ]
        if num_records > 0:
            cmd.extend(["--records", str(num_records)])
    
    # Display command
    st.code(" ".join(cmd), language="bash")
    
    # Output area
    output_container = st.container()
    status_container = st.container()
    
    try:
        with output_container:
            st.markdown("**Console Output:**")
            output_text = st.empty()
            
            # Run the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=str(scripts_path.parent)
            )
            
            st.session_state.generation_process = process
            
            output_lines = []
            start_time = time.time()
            
            # Read output in real-time
            while st.session_state.generation_active and process.poll() is None:
                try:
                    line = process.stdout.readline()
                    if line:
                        output_lines.append(line.rstrip())
                        # Keep last 100 lines
                        if len(output_lines) > 100:
                            output_lines = output_lines[-100:]
                        
                        output_text.code(
                            "\n".join(output_lines),
                            language="text"
                        )
                    time.sleep(0.1)
                except:
                    break
            
            # Get any remaining output
            remaining_output = process.stdout.read()
            if remaining_output:
                for line in remaining_output.split('\n'):
                    if line:
                        output_lines.append(line.rstrip())
            
            # Final output
            if output_lines:
                output_text.code(
                    "\n".join(output_lines[-100:]),
                    language="text"
                )
            
            # Status
            elapsed_time = time.time() - start_time
            with status_container:
                if st.session_state.generation_active and process.poll() is None:
                    st.warning(
                        f"⏳ Generation in progress... "
                        f"(Elapsed: {elapsed_time:.1f}s)\n\n"
                        f"Press **Stop Generation** button to stop."
                    )
                elif process.returncode == 0:
                    st.success(
                        f"✅ Generation completed successfully! "
                        f"(Elapsed: {elapsed_time:.1f}s)"
                    )
                    st.session_state.generation_active = False
                else:
                    st.error(
                        f"❌ Generation failed with return code {process.returncode}"
                    )
                    st.session_state.generation_active = False
    
    except Exception as e:
        st.error(f"Error running generation: {str(e)}")
        st.session_state.generation_active = False

# Footer with information
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📚 Documentation
    - **Batch Mode**: Generates a fixed number of files quickly
    - **Streaming Mode**: Generates files continuously with random delays
    """)

with col2:
    st.markdown("""
    ### 📁 Output Directory
    All generated files are saved in the `cdr_data/` directory
    - Voice CDR: `voice_cdr_mali_XX.csv`
    - SMS CDR: `sms_cdr_mali_XX.csv`
    - Data CDR: `data_cdr_mali_XX.csv`
    - Towers: `cell_towers_mali.csv`
    """)

with col3:
    st.markdown("""
    ### 💡 Tips
    - Use Batch mode for demo datasets
    - Use Streaming mode for continuous testing
    - Adjust records per file for different data volumes
    - For streaming, keep delays realistic (10-120s)
    """)

# Sidebar information
with st.sidebar:
    st.markdown("### 🔧 About")
    st.markdown("""
    **CDR Generator** is a tool for creating realistic telecom data.
    
    **Supported Types:**
    - Voice Calls (MOC/MTC)
    - SMS Messages (MO/MT)
    - Data Sessions (internet, MMS, WAP)
    
    **Features:**
    - Batch and Streaming modes
    - Configurable record counts
    - Realistic data distribution
    - Multiple regions coverage
    """)
    
    st.markdown("---")
    st.markdown("""
    **Version:** 1.0  
    **Project:** Orange Mali RFP Demo  
    **Last Updated:** January 2026
    """)
