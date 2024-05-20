import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime

def pick_files():
    # Create a root window, but keep it hidden
    root = tk.Tk()
    root.withdraw()
    
    # Open the file dialog and allow selection of multiple files
    file_paths = filedialog.askopenfilenames()  # Opens the dialog to choose multiple files
    return file_paths


selected_files = pick_files()
print("You selected:", selected_files,len(selected_files))

fixtime = input("Please add initial time in format YYYY-MM-DD HH:mm:SS.fff ...enter to goto default\n")
if fixtime == "":
    shift = False
else:
    shift = True
    dt_fix = datetime.strptime(fixtime,"%Y-%m-%d %H:%M:%S.%f")




"""
def datetime_to_seconds(dt):
    # Get seconds from hours, minutes, and seconds
    total_seconds = dt.hours * 3600 + dt.minutes * 60 + dt.seconds
    # Add microseconds as the fractional part
    total_seconds_with_ms = total_seconds + dt.microseconds / 1e6
    return total_seconds_with_ms
"""


def read_custom_csv(file_path,shift):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)  # Skip the title line
        if shift:
            for row in csv_reader:
                if row:  # Ensure the row is not empty
                    dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")  # Parse the date-time
                    dt -= dt_fix
                    sec = dt.total_seconds()
                    value = float(row[1])  # Convert the data value to float
                    data.append((sec, value))
        else: 
            row1 = next(csv_reader)
            dt_fix = datetime.strptime(row1[0], "%Y-%m-%d %H:%M:%S.%f")
            dt = datetime.strptime(row1[0], "%Y-%m-%d %H:%M:%S.%f")  # Parse the date-time
            dt -= dt_fix
            sec = dt.total_seconds()
            value = float(row1[1])  # Convert the data value to float
            data.append((sec, value))
            for row in csv_reader:
                if row:  # Ensure the row is not empty
                    dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")  # Parse the date-time
                    dt -= dt_fix
                    sec = dt.total_seconds()
                    value = float(row[1])  # Convert the data value to float
                    data.append((sec, value))
        
    return data

data_read = read_custom_csv(selected_files[0],shift)
"""
for entry in data_read:
    print(entry)
"""


def save_csv(data, headers=None):
    # Setup the root Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open a dialog to ask where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save file as"
    )

    # If a file path is provided, save the data to the file
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            if headers:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            else:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)
        print(f"Data written to CSV successfully at {file_path}")
    else:
        print("File save cancelled.")

save_csv(data_read)