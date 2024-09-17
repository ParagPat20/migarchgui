import serialio

# Open the serial port (replace '/dev/ttyUSB0' with your actual port)
with serialio.Serial('/dev/ttyUSB0', baudrate=9600) as ser:
    # Send data to the serial port
    ser.write(b'Hello from serialio!')

    # Read data from the serial port
    data = ser.read(10)
    print(data.decode())