import serial
from serial import Serial
import time

# Configure the serial port
ser = Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Function to send data to Arduino
def send_data_to_arduino(data):
    ser.write(data.encode())  # Send data encoded as bytes
    print(f"Sent: {data}")
    time.sleep(1)  # Wait for a second between sends

try:
    while True:
        # Example of sending data
        send_data_to_arduino("Hello Arduino")  # Replace with your desired message
        time.sleep(5)  # Send data every 5 seconds

except KeyboardInterrupt:
    print("Program stopped")

finally:
    ser.close()  # Close the serial connection
