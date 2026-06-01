import streamlit as st
import pandas as pd
import numpy as np
import serial
import sqlite3
import time


SERIAL_PORT = "COM3"  # declare the serial port for Arduino connection ( adjust as needed)
BAUD_RATE = 9600 # declare the baud rate for serial communication ( adjust as needed)
DB_FILE = "traffic_data.db" # declare the sqlite db file name ( To be implemented in future iterations)


# ===================== function to stream serial data from arduino to terminal ===================== #
def stream_to_terminal():


    try:
        # establish serial connection to arduino
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


        # add latency buffer to wait for the serial connection to initialize properly
        time.sleep(2) 

        # logs to terminal
        print("Connected to Arduino. Streaming data...")


        # if the serial port fails to open, display an error message and exit the function
        if not ser.is_open:
            st.error("Failed to open serial port.")
            return
        

        # continuously read from the serial port and print incoming data to the terminal
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)

        

            # add latency buffer to prevent overwhelming the terminal with too much data at once
            time.sleep(0.1)  

    

    # setup exception handling when keyboard interrupt to stop the streaming and any other unforeseen errors
    except KeyboardInterrupt:
        st.warning("Serial streaming stopped by user.")

    # catch any other exceptions and display an error message in the terminal
    except Exception as e:
        st.error(f"Error: {e}")


# run the application
if __name__ == "__main__":
    stream_to_terminal()





         



