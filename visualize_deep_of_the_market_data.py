import os
import pickle
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, AutoLocator
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import pandas as pd
import datetime
import mplfinance as mpf
import matplotlib.dates as mdates

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
                        concatenated_list.extend(data)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return concatenated_list

# Specify the directory containing the pickle files
directory = 'C:/Temp/dom request data'
scope_data = sorted(load_pickle_files(directory), key=lambda x: x[0])

# Define the column names
columns = ['open', 'high', 'low', 'close', 'volume']
# Create an empty DataFrame with these columns
df_second_candlestick = pd.DataFrame(columns=columns)
df_second_candlestick['volume'] = df_second_candlestick['volume'].astype(float)

# Create the Tkinter window
root = tk.Tk()
root.title("Bar Scatter Plot Animation")

new_figsize = (plt.rcParams["figure.figsize"][0]*2, plt.rcParams["figure.figsize"][1]*2)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=new_figsize)

bar_width = 0.00001  # Adjust as needed

# Animation control variable
is_paused = False

def toggle_animation():
    global is_paused
    is_paused = not is_paused

# Define a custom formatting function
def format_with_dots(x, pos):
    return '{:,}'.format(int(x)).replace(',', '.')

def update(frame_number):
    """Update function for the animation."""
    
    global is_paused

    # Check if the animation is paused
    if is_paused:
        # Schedule this function to be called again after 300 ms (1 second)
        root.after(300, lambda: update(frame_number))
        return

    ax1.clear()

    # Determine the range of ticks to display
    start_idx = frame_number
    end_idx = start_idx + 6

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
        ax1.set_xlim(min_price, max_price)
        ax1.set_ylim(min_volume, max_volume)

    # Number of the tick to visualize data from
    tick_number = 3

    # Your existing plotting logic, adjusted for current_data
    x1, y1 = zip(*current_data[tick_number][1])
    x2, y2 = zip(*current_data[tick_number][2])
    ax1.bar(x1, y1, width=bar_width, color='green', align='center')
    ax1.bar(x2, y2, width=bar_width, color='red', align='center')
    ax1.yaxis.grid(True, which='major')
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.5f'))
    ax1.ticklabel_format(style='plain', axis='y', useOffset=False)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_with_dots))
    ax1.yaxis.set_major_locator(AutoLocator())
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    plt.xticks(rotation=90)
    ax1.set_xlabel('Price')
    ax1.set_ylabel('Volume')
    ax1.set_title('EURUSD deep of the market')

    # Displaying the timestamp of the first element in the current range
    if current_data:
        ax1.text(min_price, max_volume * 0.95, current_data[tick_number][0], fontsize=20, color='black')
        ax1.text(min_price, max_volume * 0.85, "Ask total volume: " + f"{current_data[tick_number][3][1]:,}".replace(",", "."), fontsize=20, color='red')
        ax1.text(min_price, max_volume * 0.80, "Bid total volume: " + f"{current_data[tick_number][3][0]:,}".replace(",", "."), fontsize=20, color='green')
        ax1.text(min_price, max_volume * 0.90, "Bid: " + str(current_data[tick_number][1][0][0]), fontsize=20, color='black')

    global df_second_candlestick

    # get last element from df_second_candlestick, update its OLHCV, if the data is from
    # new second, create new element in df_second_candlestick with its values

    time_of_tick_with_miliseconds = current_data[tick_number][0]
    time_of_tick = datetime.datetime(
                                        time_of_tick_with_miliseconds.year,
                                        time_of_tick_with_miliseconds.month,
                                        time_of_tick_with_miliseconds.day,
                                        time_of_tick_with_miliseconds.hour,
                                        time_of_tick_with_miliseconds.minute,
                                        time_of_tick_with_miliseconds.second,
                                        tzinfo=time_of_tick_with_miliseconds.tzinfo
                                    )

    # get highest bid of last tick
    bid_of_last_tick = current_data[tick_number][1][0][0]
    total_volume_bid_ask_of_last_tick = current_data[tick_number][3][1] + current_data[tick_number][3][0]

    # get last element from df_second_candlestick
    if not df_second_candlestick.empty:
        # data frame is not empty
        # check if exist candlestick with current timestamp
        if time_of_tick in df_second_candlestick.index:
            # datetime of current tick exist in data frame
            if bid_of_last_tick > df_second_candlestick.at[time_of_tick, 'high']:
                df_second_candlestick.at[time_of_tick, 'high'] = bid_of_last_tick
            if bid_of_last_tick < df_second_candlestick.at[time_of_tick, 'low']:
                df_second_candlestick.at[time_of_tick, 'low'] = bid_of_last_tick
            df_second_candlestick.at[time_of_tick, 'close'] = bid_of_last_tick
            df_second_candlestick.at[time_of_tick, 'volume'] += total_volume_bid_ask_of_last_tick
        else:
            # datetime of current tick do not present in data frame
            # add new candlestick data row in df
            seconds_candlestick_ohlc = {'open': bid_of_last_tick, 'high': bid_of_last_tick, 'close': bid_of_last_tick, 'low': bid_of_last_tick, 'volume': total_volume_bid_ask_of_last_tick}
            df_second_candlestick.loc[time_of_tick] = seconds_candlestick_ohlc
    else:
        # data frame is empty, write first element to data frame
        seconds_candlestick_ohlc = {'open': bid_of_last_tick, 'high': bid_of_last_tick, 'close': bid_of_last_tick, 'low': bid_of_last_tick, 'volume': total_volume_bid_ask_of_last_tick}
        df_second_candlestick.loc[time_of_tick] = seconds_candlestick_ohlc

    # createing candlestick chart on the bottom chart
    if len(df_second_candlestick) > 1000:
        df_second_candlestick_last_n = df_second_candlestick[-100:]
    else:
        df_second_candlestick_last_n = df_second_candlestick
    
    ax2.clear()
    

    mpf.plot(df_second_candlestick_last_n, type='candle', style='charles', ax=ax2)

    # Get the current figure and axes created by mplfinance
    fig = plt.gcf()
    ax_list = fig.axes

    # Format the y-axis of the price chart (which is usually the first axes object)
    ax_list[1].yaxis.set_major_formatter(FormatStrFormatter('%.5f'))

    # Set the x-axis major formatter to display dates with hours, minutes, and seconds
    ax_list[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    #print(df_second_candlestick_last_n[:1])
    #print(df_second_candlestick_last_n)

# Create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(scope_data), interval=50, repeat=False)

# Add a pause button
pause_button = tk.Button(root, text="Pause", command=toggle_animation)
pause_button.pack()

# Tkinter event loop
root.mainloop()