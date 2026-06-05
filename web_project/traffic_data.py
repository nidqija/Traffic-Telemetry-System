import streamlit as st
import pandas as pd
import numpy as np
import serial
import sqlite3
import time
from sqlite_script import insert_data


SERIAL_PORT = "COM3"  # declare the serial port for Arduino connection ( adjust as needed)
BAUD_RATE = 9600 # declare the baud rate for serial communication ( adjust as needed)


# ===================== function to stream serial data from arduino to terminal ===================== #
def stream_to_terminal():
    ser = None
    try:
        try:
            # establish serial connection to arduino
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            print("Connected to Arduino. Streaming data...")
        except serial.SerialException as e:
            st.error(f"Error connecting to serial port {SERIAL_PORT}: {e}")
            ser = None

        # if the serial port fails to open, display an error message and use fallback logging
        if ser is None or not ser.is_open:
            st.error(
                f"Failed to open serial port {SERIAL_PORT}. Revert to simple data logging without streaming."
            )
            try:
                while True:
                    data = [
                        "12:1;7:0;8:0",
                        "12:0;7:1;8:0",
                        "12:0;7:0;8:1",
                    ]

                    for line in data:
                        process_and_log_data(line)
                        time.sleep(1)
            except KeyboardInterrupt:
                st.warning("Data logging stopped by user.")
            return

        time.sleep(2)
        print("Connection established. Starting to read data from Arduino...")
        print("Streaming data from Arduino... Press Ctrl+C to stop.")

        # continuously read from the serial port and print incoming data to the terminal
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)
                    process_and_log_data(line)  # process the incoming data and log it to the database

                # add latency buffer to prevent overwhelming the terminal with too much data at once
                time.sleep(0.1)
        except KeyboardInterrupt:
            st.warning("Serial streaming stopped by user.")

    # catch any other exceptions and display an error message in the terminal
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()



def process_and_log_data(line):
     print(line)


     try :
          timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # get the current timestamp
          parts = line.split(";")  # split the incoming data by semicolons


          state_dicts = {}

          # loop through the parts of the incoming data and extract the pin states into a dictionary for easier access,
          for part in parts:
             if ":" in part:
                      pin, state = part.split(":")  
                      state_dicts[pin.strip()] = int(state.strip())  


            # extract the pin states from dictionary , defaulting to 0 if a pin is missing from the incoming data for robustness, 
            # and insert the data into the database
          pin_12 = state_dicts.get("12", 0)
          pin_7 = state_dicts.get("7", 0) 
          pin_8 = state_dicts.get("8", 0)

          insert_data(timestamp, pin_12, pin_7, pin_8)  # insert the data into the database



     except ValueError:
          st.warning(f"Received malformed data: {line}")
          return
     
     except KeyboardInterrupt:
          st.warning("Data processing stopped by user.")
          return


# run the application
if __name__ == "__main__":

    try:
      stream_to_terminal()

    except KeyboardInterrupt:
        print("[INFO] Program exited cleanly.")





         



