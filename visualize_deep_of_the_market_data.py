import os
import pickle
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MaxNLocator
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter

def load_pickle_files(directory):
    """Load and concatenate lists from all pickle files in the given directory."""
    concatenated_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.pickle_list'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    data = pickle.load(file)
                    if isinstance(data, list):
                        concatenated_list.extend(data) #concatenated_list[0][3][0]
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return concatenated_list

# Specify the directory containing the pickle files
directory = 'C:/Temp/dom request data'
scope_data = sorted(load_pickle_files(directory), key=lambda x: x[0])
# min_price, max_price, max_volume = find_min_max_values(scope_data)

# Create the Tkinter window
root = tk.Tk()
root.title("Bar Scatter Plot Animation")
new_figsize = (plt.rcParams["figure.figsize"][0]*2, plt.rcParams["figure.figsize"][1]*2)
fig, ax = plt.subplots(figsize=new_figsize)
bar_width = 0.00001  # Adjust as needed

# Define a custom formatting function
def format_with_dots(x, pos):
    return '{:,}'.format(int(x)).replace(',', '.')

def update(frame_number):
    """Update function for the animation."""
    ax.clear()

    # Determine the range of elements to display
    start_idx = frame_number
    end_idx = start_idx + 30

    # Check if the end index exceeds the length of the data
    if end_idx > len(scope_data):
        return  # Stop updating if we've reached the end of the data

    # Extract the range of data to be visualized
    current_data = scope_data[start_idx:end_idx]

    # Calculate min and max price and volume for the current data window
    current_prices = []
    current_volumes = []
    for step in current_data:
        if len(step) > 2:  # Ensure there are at least two lists for bids and asks
            for sublist in step[1:3]:
                for item in sublist:
                    if isinstance(item, (list, tuple)) and len(item) == 2:
                        price, volume = item
                        current_prices.append(price)
                        current_volumes.append(volume)
    
    # Calculate min and max for the current frame
    if current_prices and current_volumes:
        min_price = min(current_prices)
        max_price = max(current_prices)
        min_volume = min(current_volumes)
        max_volume = max(current_volumes)
        ax.set_xlim(min_price, max_price)
        ax.set_ylim(min_volume, max_volume)

    # Set the limits for the x-axis and y-axis
    ax.set_xlim(min_price, max_price)
    ax.set_ylim(min_volume, max_volume)

    # Your existing plotting logic, adjusted for current_data
    for step in current_data:
        if len(step) > 2:
            x1, y1 = zip(*step[1])
            x2, y2 = zip(*step[2])
            ax.bar(x1, y1, width=bar_width, color='green', align='center')
            ax.bar(x2, y2, width=bar_width, color='red', align='center')
    
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.5f'))
    ax.ticklabel_format(style='plain', axis='y', useOffset=False)
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_dots))
    ax.xaxis.set_major_locator(MaxNLocator(30))
    ax.yaxis.set_major_locator(MaxNLocator(30))
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    plt.xticks(rotation=90)
    ax.set_xlabel('Price')
    ax.set_ylabel('Volume')
    ax.set_title('EURUSD deep of the market')
    # Displaying the timestamp of the first element in the current range
    if current_data:
        ax.text(min_price, max_volume * 0.9, current_data[0][0], fontsize=30, color='blue')
        ax.text(min_price, max_volume * 0.8, "Ask: " + f"{current_data[0][3][1]:,}".replace(",", "."), fontsize=30, color='blue')
        ax.text(min_price, max_volume * 0.7, "Bid: " + f"{current_data[0][3][0]:,}".replace(",", "."), fontsize=30, color='blue')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
ani = animation.FuncAnimation(fig, update, frames=len(scope_data), interval=100, repeat=False)
root.mainloop()