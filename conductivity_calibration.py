import serial
import time

# Initialize serial communication
PORTNAME = '/dev/ttyUSB1'  # Adjust the port name as needed
ser = serial.Serial(PORTNAME, 9600, timeout=1)

def send_command(command):
    """Send a command to the EZO-EC module and return the response."""
    ser.write(command.encode('utf-8'))
    time.sleep(3)  # Wait for the command to be processed
    response = ser.read_all().decode('utf-8').strip()
    return response

def calibrate_ec():
    """Perform 3-point calibration for the EC sensor."""
    calibration_points = [
        ('dry', None),
        ('low', 12880),  # Example low point value in μS
        ('high', 80000)  # Example high point value in μS
    ]

    for point, value in calibration_points:
        if point == 'dry':
            command = f'Cal,{point}\r'
        else:
            command = f'Cal,{point},{value}\r'
        response = send_command(command)
        print(f'Calibration {point} ({value}): {response}')
        
        if '*OK' not in response:
            print(f'Calibration for {point} point (value {value}) failed.')
            return False
        
    print('3-point calibration successful.')
    return True

if __name__ == '__main__':
    if calibrate_ec():
        print("Calibration completed successfully.")
    else:
        print("Calibration failed.")
