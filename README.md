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

6. start a new background session by typing the following in the command line, replacing _mysession_ with your desired session name (name is arbitrary):

    tmux new -s mysession

7. run the reading scripts for ph and conductivity

    python3 ph_and_conductivity_reading.py

    log csv files will be produced

    naming convention is {sensor_type}\_log\_{current_time}.csv

8. to view the dashboard, go into your browser and navigate to 127.0.0.1:8050

    you can close out of this browser at any time and no data will be lost !


# tmux setup steps / help
screen is a tool used to create sessions that run in the background, so even if connections via ssh are lost, the session / programs run will still continue

1. start a new background session by typing the following in the command line, replacing _mysession_ with your desired session name (arbitrary):
  
    tmux new -s mysession


2. to detach from the "mysession", press _Ctrl + B_, then _D_

    this will let you access the "main" session, and not interfere with the "mysession"

3. to reattach to the "screen session" if detached, type the following in the command line:

    tmux attach -t mysession


4. to list all running "tmux sessions", type:

    tmux ls

5. to terminate a specific screen session, use the following, replacing _mysession_ with the name of the session:

    tmux kill-session -t mysession


    to verify the session has been terminated, type:
  
      tmux -ls

6. to kill all tmux sessions, use:

    tmux kill-server

