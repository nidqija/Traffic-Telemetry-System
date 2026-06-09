import streamlit as st
from traffic_data import stream_to_terminal
from sqlite_script import get_all_data
import pandas as pd
import asyncio

st.set_page_config(
    page_title="Traffic Telemetry",
    page_icon="🚦",
    layout="wide"  # Uses more screen real estate
)


st.markdown("""
    <style>
    /* Make headers pop a bit more */
    .main-title {
        font-size: 100px !important;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .subtitle {
        color: #64748B;
        font-size: 25px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)


@st.fragment
def home():
    st.title("🚦 Traffic Telemetry Dashboard", anchor="main-title")
    st.subheader("Real-Time Traffic Light Status and Data Log", anchor="subtitle")

    # Fetch data
    data_rows = asyncio.run(get_all_data())

    if not data_rows:
        st.info("No data available yet. Please wait for the Arduino to send data. ⏳")
    else:
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=["ID", "Timestamp", "Pin 12 (Red)", "Pin 7 (Green)", "Pin 8 (Yellow)"])
        
        # Get the absolute latest status for the metrics
        latest_row = df.iloc[-1]
        
        # --- STYLING LAYOUT: METRIC CARDS ---
        st.subheader("Current Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            red_status = "🔴 ACTIVE" if latest_row["Pin 12 (Red)"] in [1, "1", "HIGH"] else "⚫ OFF"
            st.metric(label="Red Light (Pin 12)", value=red_status)
            
        with col2:
            yellow_status = "🟡 ACTIVE" if latest_row["Pin 8 (Yellow)"] in [1, "1", "HIGH"] else "⚫ OFF"
            st.metric(label="Yellow Light (Pin 8)", value=yellow_status)
            
        with col3:
            green_status = "🟢 ACTIVE" if latest_row["Pin 7 (Green)"] in [1, "1", "HIGH"] else "⚫ OFF"
            st.metric(label="Green Light (Pin 7)", value=green_status)

        st.divider() 

        st.subheader("📊 Real-Time Traffic Data Log")
        
        # Sort by latest timestamp first for better UX
        df_sorted = df.sort_values(by="Timestamp", ascending=False)
        st.dataframe(df_sorted, use_container_width=True, hide_index=True)  

    # Terminal stream call
    stream_to_terminal()



if __name__ == "__main__":
    home()