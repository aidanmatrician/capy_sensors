# capy_sensors

Conductivity and ph probes are from AtlasScientific.

# set up steps

1. plug in raspberry pi

2. plug in ph sensor to usb port on raspberry pi

3. plug in conductivity sensor to usb port on raspberry pi

4. ssh (login) to raspberry pi with the following command, replacing ip_address with the address of the pi:

    ssh -L 8050:localhost:8050 boer@<ip_address>

5. run calibration scripts if needed 

    python3 ph_calibration.py

    python3 conductivity_calibration.py

6. start a new screen session by typing the following in the command line:

    screen

7. run the reading scripts for ph and conductivity

    python3 ph_and_conductivity_reading.py

    log csv files will be produced

    naming convention is {sensor_type}\_log\_{current_time}.csv


# screen setup steps / help
screen is a tool used to create sessions that run in the background, so even if connections via ssh are lost, the session / programs run will still continue

1. start a new screen session by typing the following in the command line:
  
    screen

2. to detach from the "screen session", press _Ctrl + A_, then _D_

    this will let you access the "main" session, and not interfere with the "screen session"

3. to reattach to the "screen session" if detached, type the following in the command line:

    screen -r

4. to list all running "screen sessions", type:

    screen -ls

  the output should look something like this:

    There are screens on:
      1234.pts-0.yourhostname (Attached)
      5678.pts-1.yourhostname (Detached)
    2 Sockets in /run/screen/S-yourusername.

5. to terminate a specific screen session, use the following, replacing _pid_ with the process id of the screen you want to remove:

    screen -X -S _pid_ quit

    for example, if we wanted to terminate the first screen, we would type the command:

    screen -X -S 1234 quit

    to verify the session has been terminated, type:
  
      screen -ls
