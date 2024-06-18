import serial
import datetime

# Initialize serial communication
PORTNAME = '/dev/ttyUSB0' # Adjust the port name as needed
ser = serial.Serial(PORTNAME, 9600, timeout=1)
print(ser)
def read_ph():
    print('started read_ph() at ' + datetime.datetime.now())

    # Send a command to the EZO module to take a reading
    ser.write(b'R\r')
    print('wrote command to EZO module')
    time.sleep(1.5)  # Wait for the reading to complete
    
    # Read the data from the EZO module
    data = ser.readline().decode('utf-8').strip()
    print('data returned from reading: ' + data)
    
    return data

if __name__ == "__main__":
    while True:
        ph_value = read_ph()
        print("pH Value:", ph_value)
        time.sleep(5)  # Take a reading every 5 seconds
