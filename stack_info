import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime, timedelta
import os

def pick_files():
    # Create a root window, but keep it hidden
    root = tk.Tk()
    root.withdraw()
    
    # Open the file dialog and allow selection of multiple files
    file_paths = filedialog.askopenfilenames()  # Opens the dialog to choose multiple files
    return file_paths

def julian_day_to_datetime(jd):
    # Calculation constants
    JD_JAN_1_4713_BC = 2400000.5
    seconds_per_day = 86400
    
    # Adjusting for the half-day offset
    jd = jd + 0.5
    
    # Calculate the integer part (days) and fractional part (time)
    jdn = int(jd)
    fractional_day = jd - jdn
    
    # Algorithm to convert Julian Day Number to Gregorian date
    L = jdn + 68569
    N = 4 * L // 146097
    L = L - (146097 * N + 3) // 4
    I = 4000 * (L + 1) // 1461001
    L = L - 1461 * I // 4 + 31
    J = 80 * L // 2447
    day = L - 2447 * J // 80
    L = J // 11
    month = J + 2 - 12 * L
    year = 100 * (N - 49) + I + L

    # Calculate time from the fractional day
    seconds_in_day = fractional_day * seconds_per_day
    hour = int(seconds_in_day // 3600)
    minute = int((seconds_in_day % 3600) // 60)
    second = seconds_in_day % 60
    
    # Return datetime object
    return datetime(year, month, day, hour, minute, int(second), int((second - int(second)) * 1e6))

def save_csv(data,orifilename=None,headers=None):
    # Setup the root Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open a dialog to ask where to save the file
    file_path = filedialog.asksaveasfilename(
        initialfile=orifilename,
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

print("This file reads the info file extracted from ImageJ opened nd2 file.\n")
print("You can open multiple files at the same time. \n")
print("It turns txt file to csv file\n")

# ask if need to subtract a fixed time, default will start from 0
fixtime = input("Please add initial time in format YYYY-MM-DD HH:mm:SS.fff ...enter to goto default\n")
if fixtime == "":
    shift = False
else:
    shift = True
    dt_fix = datetime.strptime(fixtime,"%Y-%m-%d %H:%M:%S.%f")


# define keyword for the absolute start time 
file_path = pick_files()
keyword1 = 'dTimeAbsolute'
keyword2 = 'timestamp'

for i in range(len(file_path)):

    reftimelist = []
    count = 1

    # Read the file and search for the keyword
    with open(file_path[i], 'r') as file:
        for line in file:
            if keyword1 in line:
                abstime = float(line.split('=')[1].strip())
                print(f"{keyword1} = {abstime}")
            elif keyword2 in line:
                reftime = float(line.split(' ')[3].strip())
                reftimelist.append((count,reftime))
                count += 1

    abstime_greg_utc = julian_day_to_datetime(abstime)
    abstime_greg_est = abstime_greg_utc - timedelta(hours=4)
    print("Corresponding Gregorian datetime(EST):", abstime_greg_est)
    orifilename = os.path.splitext(os.path.split(file_path[i])[1])[0]
    print(orifilename)
    shifttimelist = []
    if shift:
        deltatime = abstime_greg_est - dt_fix 
        im_diff = deltatime.total_seconds()
        for i in range(len(reftimelist)):
            refref = im_diff + reftimelist[i][1]
            gregtime = abstime_greg_est + timedelta(seconds=reftimelist[i][1])
            shifttimelist.append((i+1,refref,gregtime))
        save_csv(shifttimelist,orifilename)
    else: 
        for i in range(len(reftimelist)):
            gregtime = abstime_greg_est + timedelta(seconds=reftimelist[i][1])
            shifttimelist.append((i+1,reftimelist[i][1],gregtime))
        save_csv(shifttimelist,orifilename)
