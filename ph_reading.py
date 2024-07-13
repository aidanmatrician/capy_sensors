import serial
import time
import csv
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime

# Initialize serial communication
PORTNAME = '/dev/ttyUSB0'  # Adjust the port name as needed
ser = serial.Serial(PORTNAME, 9600, timeout=1)

def generate_filename():
    """Generate a unique filename based on the current date and time."""
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'ph_log_{current_time}.csv'
    return filename

def read_ph():
    """Read pH value from the EZO module."""
    ser.write(b'R\r')
    time.sleep(1.5)  # Wait for the reading to complete
    
    # Read the data from the EZO module
    data = ser.read_all().decode('utf-8').strip()
    
    # Extract the latest pH value from the data
    readings = data.split('\r')
    latest_reading = readings[-1].strip() if readings else None
    
    # Check if the latest reading is a valid float
    try:
        return float(latest_reading)
    except ValueError:
        return None

def read_csv(file_path):
    """Read historical data from CSV file."""
    time_list = []
    ph_list = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if len(row) == 2:
                    time_list.append(row[0])
                    ph_list.append(float(row[1]))
    except FileNotFoundError:
        pass
    return time_list, ph_list

# Generate a unique filename for the new log file
file_path = generate_filename()

# Initialize the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-Time pH Value"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=3.5*1000,  # Update every 3.5 seconds
        n_intervals=0
    )
])

@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    start_time = time.time()  # Record the start time

    ph_value = read_ph()
    if ph_value is not None:
        # Write the current time and pH value to the CSV file
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                writer.writerow(["Time", "pH Value"])  # Write the header
            writer.writerow([current_time, ph_value])

    # Read the CSV file to get the full history
    time_list, ph_list = read_csv(file_path)

    # Limit the display to the most recent 100 entries to keep the plot manageable
    time_list = time_list[-100:]
    ph_list = ph_list[-100:]

    fig = go.Figure(
        data=[go.Scatter(x=time_list, y=ph_list, mode='lines+markers', name='pH Value')],
        layout=go.Layout(
            title="Real-Time pH Value",
            xaxis_title="Time",
            yaxis_title="pH"
        )
    )

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Time elapsed for this interval: {elapsed_time:.2f} seconds")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
