import streamlit as st
from traffic_data import stream_to_terminal





def home():
    st.title("Traffic Light Monitoring System")
    st.write("Welcome to TrafficTelemetry!")


    st.subheader("Real-Time Traffic Data Stream")
    st.write("Review the real-time traffic data stream from the Arduino below:")
    stream_to_terminal()



if __name__ == "__main__":
    home()
    