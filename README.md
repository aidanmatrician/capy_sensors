# capy_sensors

Conductivity and ph probes are from AtlasScientific.

# how to set up
1. plug in raspberry pi
2. plug in ph sensor to usb port on raspberry pi
3. plug in conductivity sensor to usb port on raspberry pi
4. run calibration scripts if needed 
  python3 ph_calibration.py
  python3 conductivity_calibration.py
5. run ph_and_conductivity_reading.py
  python3 ph_and_conductivity_reading.py
6. when cycle is complete, CTRL + C to terminate program
  log csv files will be produced
  naming convention is {sensor_type}\_log\_{current_time}.csv
