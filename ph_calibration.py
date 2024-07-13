import serial
import time

# Initialize serial communication
PORTNAME = '/dev/ttyUSB0'  # Adjust the port name as needed
ser = serial.Serial(PORTNAME, 9600, timeout=1)

def send_command(command):
    """Send a command to the EZO-pH module and return the response."""
    ser.write(command.encode('utf-8'))
    time.sleep(3)  # Wait for the command to be processed
    response = ser.read_all().decode('utf-8').strip()
    return response

def calibrate_ph():
    """Perform 3-point calibration for the pH sensor."""
    calibration_points = [
        ('low', 4.00),
        ('mid', 7.00),
        ('high', 10.00)
    ]

    for point, value in calibration_points:
        command = f'Cal,{point},{value:.2f}\r'
        response = send_command(command)
        print(f'Calibration {point} ({value}): {response}')
        
        if '*OK' not in response:
            print(f'Calibration for {point} point (pH {value}) failed.')
            return False
        
    print('3-point calibration successful.')
    return True

if __name__ == '__main__':
    if calibrate_ph():
        print("Calibration completed successfully.")
    else:
        print("Calibration failed.")
