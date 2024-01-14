"""
1. Read picklefiles with dom data
2. Conncatenate all lists in unique list
3. Order all elements of the list by index element of each tick
4. Create Tkinter form, create canvas
5. Create deep of the market image in loop, go thru all ticks and visualize dom data
"""

import os
import pickle
import tkinter as tk

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

directory = 'C:/Temp/dom request data'
scope_data = sorted(load_pickle_files(directory), key=lambda x: x[0]) # sort of tickes based on index

def draw_dom_data_on_canvas (canvas, dom_data):
    """draw dom data on the canvas"""
    # logic of how many ticks can be visualized on width of canvas
    canvas_with = 3072
    n_tick = len(dom_data) - 1
    while ((canvas_with > 0) and (n_tick >= 0)):
        bid_prices, bid_volumes = zip(*dom_data[n_tick][1])
        ask_prices, ask_volumes = zip(*dom_data[n_tick][2])
        # scaling here volume 500.000 to one pixel
        bid_volumes_pixels = [round(element / 500000) for element in bid_volumes]
        ask_volumes_pixels = [round(element / 500000) for element in ask_volumes]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        canvas_with -= max_volume_pixel - 1
        # can not draw to the left
        if canvas_with - max_volume_pixel <= 0:
            break
        n_tick -= 1
    # find max and min prices among all ticks
    range_of_ticks_to_draw = dom_data[n_tick+1:len(dom_data)]
    max_price = max([pair[0] for sublist in [tick_data[2]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    min_price = min([pair[0] for sublist in [tick_data[1]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    # draw all tick data on canvas
    canvas_with = 3072
    for index in range(len(range_of_ticks_to_draw)-1, -1, -1):
        bid_prices, bid_volumes = zip(*range_of_ticks_to_draw[index][1])
        ask_prices, ask_volumes = zip(*range_of_ticks_to_draw[index][2])
        # scaling here volume 500.000 to one pixel
        bid_volumes_pixels = [round(element / 500000) for element in bid_volumes]
        ask_volumes_pixels = [round(element / 500000) for element in ask_volumes]
        # Pixel range
        min_pixel_vertical = 1
        max_pixel_vertical = 1664
        # Calculate scaling factor
        scaling_factor = (max_pixel_vertical - min_pixel_vertical) / (max_price - min_price)
        # Map each price to its pixel value
        bid_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in bid_prices]
        ask_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in ask_prices]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        bid_volume_pixels = list(zip(bid_pixels, bid_volumes_pixels))
        ask_volume_pixels = list(zip(ask_pixels, ask_volumes_pixels))
        top_left_coordinate_left = canvas_with - max_volume_pixel -1
        # drawing volumes on the left
        [canvas.create_rectangle(top_left_coordinate_left, price_bid_pixel, top_left_coordinate_left + volume_bid_pixel, price_bid_pixel+10, fill="green") for price_bid_pixel, volume_bid_pixel in bid_volume_pixels] #bids
        [canvas.create_rectangle(top_left_coordinate_left, price_ask_pixel, top_left_coordinate_left + volume_ask_pixel, price_ask_pixel+10, fill="red") for price_ask_pixel, volume_ask_pixel in ask_volume_pixels] #asks
        canvas_with = top_left_coordinate_left

root = tk.Tk()
root.title("EUR USD deep of the market")
root.state('zoomed') # Maximize the window
canvas = tk.Canvas(root, bg='black')
canvas.pack(fill='both', expand=True)  # Fill and expand in both directions
draw_dom_data_on_canvas(canvas, scope_data[:400])
    
root.mainloop()







# scope_data[1][0] # index
# scope_data[1][1] # bid values
# scope_data[1][2] # ask values
# scope_data[1][3] # total bid ask values

# coord 1,2,3,4
# 1,2 is top-left corner coordinate (left-right, top-down)
# 3,4 is bottom-right corner coordinate (left-right, top-down) 
# canvas.create_rectangle(50, 150, 150, 150, fill="blue")

