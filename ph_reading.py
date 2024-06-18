import serial
import time

# Initialize serial communication
PORTNAME = '/dev/ttyUSB0' # Adjust the port name as needed
ser = serial.Serial(PORTNAME, 9600, timeout=1) 

def read_ph():
    # Send a command to the EZO module to take a reading
    ser.write(b'R\r')
    time.sleep(1.5)  # Wait for the reading to complete
    
    # Read the data from the EZO module
    data = ser.readline().decode('utf-8').strip()
    
    return data

if __name__ == "__main__":
    while True:
        ph_value = read_ph()
        print("pH Value:", ph_value)
        time.sleep(5)  # Take a reading every 5 seconds
