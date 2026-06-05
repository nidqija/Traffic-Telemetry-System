import time


while True:
        # simulate streaming data from Arduino by printing predefined data every second
        # fallback to this loop if the serial port fails to open, allowing us to test the rest of the data handling and dashboard functionality without needing an active Arduino connection
        data = [[
                    "12:1",
                    "7:0",
                    "8:0"
                ] , [
                    "12:0",
                    "7:1",
                    "8:0"
                ] , [
                    "12:0",
                    "7:0",
                    "8:1"
                ]]  

        
        for line in data:
                    print(line)
                    time.sleep(1)  



