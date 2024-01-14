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

def run_tkinter_form (dom_data):
    """Create tkinter form, visualize data of dom."""
    
    def draw_one_tick_data_on_the_canvas (canvas, tick):
        """draw data of one tick on the canvas"""
        canvas_resolution =  [3072, 1665]
        index = tick[0]
        bid_prices, bid_volumes = zip(*tick[1])
        ask_prices, ask_volumes = zip(*tick[2])
        total_volumes = tick[3]
        max_price = max(ask_prices)
        min_price = min(bid_prices)
        # scaling here 500.000 to one
        bid_volumes_pixels = [round(element / 500000) for element in bid_volumes]
        ask_volumes_pixels = [round(element / 500000) for element in ask_volumes]
        # Pixel range
        min_pixel_vertical = 1
        max_pixel_vertical = canvas_resolution[1] - 1
        # Calculate scaling factor
        scaling_factor = (max_pixel_vertical - min_pixel_vertical) / (max_price - min_price)
        # Map each price to its pixel value
        bid_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in bid_prices]
        ask_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in ask_prices]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        bid_volume_pixels = list(zip(bid_pixels, bid_volumes_pixels))
        ask_volume_pixels = list(zip(ask_pixels, ask_volumes_pixels))
        top_left_coordinate_left = canvas_resolution[0] - max_volume_pixel
        # drawing volumes on the left
        [canvas.create_rectangle(top_left_coordinate_left, price_bid_pixel, top_left_coordinate_left + volume_bid_pixel, price_bid_pixel+10, fill="green") for price_bid_pixel, volume_bid_pixel in bid_volume_pixels] #bids
        [canvas.create_rectangle(top_left_coordinate_left, price_ask_pixel, top_left_coordinate_left + volume_ask_pixel, price_ask_pixel+10, fill="red") for price_ask_pixel, volume_ask_pixel in ask_volume_pixels] #asks
        print(bid_prices, ask_prices)
        print(bid_pixels, ask_pixels)
        print("")
    
    def draw_dom_data_on_canvas (canvas, dom_data, index= 0):
        """draw dom data on the canvas"""
        if index < len(dom_data):
            draw_one_tick_data_on_the_canvas(canvas, dom_data[index])
            # Schedule the next tick after a delay
            canvas.after(1000, lambda: draw_dom_data_on_canvas(canvas, dom_data, index + 1))
    
    root = tk.Tk()
    root.title("EUR USD deep of the market")
    root.state('zoomed') # Maximize the window
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill='both', expand=True)  # Fill and expand in both directions
    draw_dom_data_on_canvas(canvas, dom_data)
    root.mainloop()

run_tkinter_form (scope_data[:5])







# scope_data[1][0] # index
# scope_data[1][1] # bid values
# scope_data[1][2] # ask values
# scope_data[1][3] # total bid ask values

# coord 1,2,3,4
# 1,2 is top-left corner coordinate (left-right, top-down)
# 3,4 is bottom-right corner coordinate (left-right, top-down) 
# canvas.create_rectangle(50, 150, 150, 150, fill="blue")

