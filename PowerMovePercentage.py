import tkinter as tk
from tkinter import filedialog
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Define custom tkinter style
custom_style = {
    'font': ('Arial', 12),
    'bg': '#f0f0f0',
    'padx': 10,
    'pady': 5,
}

# Function to calculate kWh
def calculate_kwh():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if not file_path:
        return

    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    try:
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time = datetime.strptime(end_time, "%H:%M:%S")
    except ValueError:
        result_text.set("Invalid time format. Please use HH:MM:SS.")
        return

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert the dateTime column to datetime objects
    df['dateTime'] = pd.to_datetime(df['dateTime'])

    # Get the current date in UTC timezone
    current_datetime = datetime.now(pytz.utc)

    # Get the start of the current month in UTC timezone
    current_month_start = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get the start of the next month in UTC timezone
    next_month_start = (current_month_start + pd.DateOffset(months=1))

    # Filter rows for the current month
    current_month_df = df[
        (df['dateTime'] >= current_month_start) &
        (df['dateTime'] < next_month_start)
    ]

    # Filter rows for the current month and between user-defined start and end times
    filtered_df = current_month_df[
        (current_month_df['dateTime'].dt.time >= start_time.time()) &
        (current_month_df['dateTime'].dt.time < end_time.time())
    ]

    # Calculate the total kWh for the current month
    TotalMonthkWh = current_month_df['kWh'].sum()

    # Calculate the total kWh between user-defined start and end times for the current month
    TotalPowerMove = filtered_df['kWh'].sum()

    # Calculate the percentage
    percentage = (TotalPowerMove / TotalMonthkWh) * 100

    result_text.set(
        f'Total kWh for the current month: {TotalMonthkWh:.2f}\n'
        f'Total kWh between {start_time.strftime("%H:%M:%S")} and {end_time.strftime("%H:%M:%S")} '
        f'for the current month: {TotalPowerMove:.2f}\n'
        f'Percentage of TotalPowerMove compared to TotalMonthkWh: {percentage:.2f}%'
    )

# Create the main window
root = tk.Tk()
root.title("KWh Calculator")

# Set custom style
root.option_add("*TButton*Font", custom_style['font'])
root.option_add("*TButton*Background", custom_style['bg'])
root.option_add("*TButton*Padding", (custom_style['padx'], custom_style['pady']))

# Create a custom style frame
style_frame = tk.Frame(root, bg=custom_style['bg'])
style_frame.pack(pady=20)

# Create a custom style label
style_label = tk.Label(
    style_frame,
    text="KWh Calculator",
    font=("Arial", 18),
    bg=custom_style['bg']
)
style_label.pack()

# Create input fields for start and end times with default values
start_time_label = tk.Label(
    style_frame,
    text="Start Time (HH:MM:SS):",
    font=("Arial", 12),
    bg=custom_style['bg']
)
start_time_label.pack()

start_time_entry = tk.Entry(style_frame, font=("Arial", 12))
start_time_entry.insert(0, "16:00:00")  # Set default start time
start_time_entry.pack()

end_time_label = tk.Label(
    style_frame,
    text="End Time (HH:MM:SS):",
    font=("Arial", 12),
    bg=custom_style['bg']
)
end_time_label.pack()

end_time_entry = tk.Entry(style_frame, font=("Arial", 12))
end_time_entry.insert(0, "19:00:00")  # Set default end time
end_time_entry.pack()

# Create a custom style button
style_button = tk.Button(
    style_frame,
    text="Browse for CSV File",
    command=calculate_kwh,
    font=("Arial", 14),
    bg="#007acc",
    fg="white",
)
style_button.pack(pady=10)

# Create a custom style label for displaying results
result_text = tk.StringVar()
result_label = tk.Label(
    root,
    textvariable=result_text,
    font=("Arial", 12),
    bg=custom_style['bg'],
    justify="left"
)
result_label.pack(padx=20, pady=10)

root.mainloop()
