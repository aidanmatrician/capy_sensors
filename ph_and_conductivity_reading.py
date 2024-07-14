import serial
import time
import csv
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime

# Initialize serial communications
ser_ph = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # pH module
ser_ec = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)  # EC module

def generate_filename(sensor_type):
    """Generate a unique filename based on the current date and time."""
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{sensor_type}_log_{current_time}.csv'
    return filename

def read_ph():
    """Read pH value from the EZO-pH module."""
    ser_ph.write(b'R\r')
    time.sleep(1.5)  # Wait for the reading to complete
    data = ser_ph.read_all().decode('utf-8').strip()
    readings = data.split('\r')
    latest_reading = readings[-1].strip() if readings else None
    try:
        return float(latest_reading)
    except ValueError:
        return None

def read_ec():
    """Read EC value from the EZO-EC module."""
    ser_ec.write(b'R\r')
    time.sleep(1.5)  # Wait for the reading to complete
    data = ser_ec.read_all().decode('utf-8').strip()
    readings = data.split('\r')
    latest_reading = readings[-1].strip() if readings else None
    try:
        return float(latest_reading)
    except ValueError:
        return None

def read_csv(file_path):
    """Read historical data from CSV file."""
    time_list = []
    value_list = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if len(row) == 2:
                    time_list.append(row[0])
                    value_list.append(float(row[1]))
    except FileNotFoundError:
        pass
    return time_list, value_list

# Generate unique filenames for the new log files
ph_file_path = generate_filename('ph')
ec_file_path = generate_filename('ec')

# Initialize the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-Time pH and EC Values"),
    dcc.Graph(id='live-ph-graph'),
    dcc.Graph(id='live-ec-graph'),
    dcc.Interval(
        id='interval-component',
        interval=3.5*1000,  # Update every 3.5 seconds
        n_intervals=0
    )
])

@app.callback(
    [Output('live-ph-graph', 'figure'),
     Output('live-ec-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):
    start_time = time.time()  # Record the start time

    ph_value = read_ph()
    ec_value = read_ec()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if ph_value is not None:
        with open(ph_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                writer.writerow(["Time", "pH Value"])  # Write the header
            writer.writerow([current_time, ph_value])
    if ec_value is not None:
        with open(ec_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                writer.writerow(["Time", "EC Value"])  # Write the header
            writer.writerow([current_time, ec_value])

    # Read the CSV files to get the full history
    ph_time_list, ph_value_list = read_csv(ph_file_path)
    ec_time_list, ec_value_list = read_csv(ec_file_path)

    ph_fig = go.Figure(
        data=[go.Scatter(x=ph_time_list, y=ph_value_list, mode='lines+markers', name='pH Value')],
        layout=go.Layout(
            title="Real-Time pH Value",
            xaxis_title="Time",
            yaxis_title="pH"
        )
    )

    ec_fig = go.Figure(
        data=[go.Scatter(x=ec_time_list, y=ec_value_list, mode='lines+markers', name='EC Value')],
        layout=go.Layout(
            title="Real-Time EC Value",
            xaxis_title="Time",
            yaxis_title="EC (μS/cm)"
        )
    )

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Time elapsed for this interval: {elapsed_time:.2f} seconds")

    return ph_fig, ec_fig

if __name__ == '__main__':
    app.run_server(debug=True)
