import os
import pickle
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter, MaxNLocator
import matplotlib.animation as animation

# Specify the directory containing the pickle files
directory = 'C:/Temp/dom request data'

# Initialize an empty list to store the concatenated data
concatenated_list = []

# List all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):  # Check for pickle files
        filepath = os.path.join(directory, filename)
        with open(filepath, 'rb') as file:
            try:
                # Load the list from the pickle file
                data = pickle.load(file)
                if isinstance(data, list):  # Check if the data is a list
                    concatenated_list.extend(data)  # Concatenate the list
            except Exception as e:
                print(f"Error loading {filename}: {e}")

# This should be your actual data sequence
scope_data = concatenated_list
scope_data = sorted(scope_data, key=lambda x: x[0])

#visualize data of by bunches
first_number_of_bunch = 0
last_number_of_bunch = 100

# Initialize min and max values
min_price = float('inf')
max_price = float('-inf')
max_volume = float('-inf')

# Loop through each step in the data sequence to find min/max values
for step in scope_data:
    if len(step) > 2:  # Ensure there are at least two lists for bids and asks
        for sublist in step[1:3]:  # Check only the second and third lists for bids and asks
            prices, volumes = zip(*sublist)
            min_price = min(min_price, *prices)
            max_price = max(max_price, *prices)
            max_volume = max(max_volume, *volumes)

# Create the Tkinter window
root = tk.Tk()
root.title("Bar Scatter Plot Animation")

# Double the size of the figure
current_figsize = plt.rcParams["figure.figsize"]
new_figsize = (current_figsize[0]*2, current_figsize[1]*2)

# Create the Matplotlib figure and axes
fig, ax = plt.subplots(figsize=new_figsize)
ax.set_xlim(min_price, max_price)
ax.set_ylim(0, max_volume)

bar_width = 0.00001  # Adjust as needed

# Define the update function for the animation
def update(frame_number):
    ax.clear()
    ax.set_xlim(min_price, max_price)
    ax.set_ylim(0, max_volume)
    
    # Ensure the frame number doesn't exceed the length of the dataset
    if frame_number < len(scope_data):
        step = scope_data[frame_number]
        if len(step) > 2:  # Ensure there are at least two lists for bids and asks
            x1, y1 = zip(*step[1])
            x2, y2 = zip(*step[2])
            ax.bar(x1, y1, width=bar_width, color='green', align='center')
            ax.bar(x2, y2, width=bar_width, color='red', align='center')

            # Set the x-axis formatter
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.5f'))

            # Set the maximum number of x-axis and y-axis ticks
            ax.xaxis.set_major_locator(MaxNLocator(30))  # Adjust the number 15 as needed
            ax.yaxis.set_major_locator(MaxNLocator(30))  # Adjust the number 10 as needed            

            # Enable grid only for the x-axis
            ax.xaxis.grid(True)

            # Enable grid only for the y-axis
            ax.yaxis.grid(True)

            # Rotate x-axis labels to be vertical
            plt.xticks(rotation=90)
    
    ax.set_xlabel('Price')
    ax.set_ylabel('Volume')
    ax.set_title('EURUSD deep of the market')
    x_position = min_price
    #x_position = (min_price + max_price) / 2
    y_position = max_volume * 0.9
    ax.text(x_position, y_position, step[0], fontsize=30, color='blue')

# Create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(scope_data), interval=50, repeat=False)

# Tkinter event loop
root.mainloop()





