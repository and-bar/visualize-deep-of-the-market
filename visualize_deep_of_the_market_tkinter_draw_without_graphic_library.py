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

def draw_dom_data_on_canvas (canvas, dom_data_full, end_tick_bar_to_draw):
    """draw dom data on the canvas"""
    # logic of how many ticks can be visualized on width of canvas
    if canvas.winfo_width() == 1:
        maximum_with_canvas = 1000
        max_pixel_vertical = 950
    else:
        maximum_with_canvas = canvas.winfo_width()
        max_pixel_vertical = canvas.winfo_height()
    # getting info how many tick can fir into canvas with
    canvas_with_left = maximum_with_canvas #3840
    dom_data = dom_data_full[:end_tick_bar_to_draw]
    lenght_ofdom_data_elements = len(dom_data)
    n_tick = lenght_ofdom_data_elements - 1
    while ((canvas_with_left > 0) and (n_tick >= 0)):
        bid_prices, bid_volumes = zip(*dom_data[n_tick][1])
        ask_prices, ask_volumes = zip(*dom_data[n_tick][2])
        # scaling here volume n000000 to one pixel
        one_pixel_equeal_n_volume = 100000
        bid_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        canvas_with_left -= max_volume_pixel - 1
        # can not draw to the left
        if canvas_with_left - max_volume_pixel <= 0:
            break
        n_tick -= 1
        
    n_of_ticks_to_visualize = lenght_ofdom_data_elements - n_tick+1
    print("n of ticks to draw: ", n_of_ticks_to_visualize)
    start_index_tick_data = n_tick+1
    #print("start_index_tick_data: ", start_index_tick_data)
    # find max and min prices among all ticks
    range_of_ticks_to_draw = dom_data[start_index_tick_data:lenght_ofdom_data_elements]
    max_price = max([pair[0] for sublist in [tick_data[2]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    min_price = min([pair[0] for sublist in [tick_data[1]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    # print("all ask prices: ", [pair[0] for sublist in [tick_data[1]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    # print("min price: ", min_price, " max price: ", max_price)
    # draw all tick data on canvas
    canvas.delete("all")
    canvas_with_left = maximum_with_canvas #3840
    #one_pixel_equeal_n_volume = 20000
    for index in range(len(range_of_ticks_to_draw)-1, -1, -1):
        bid_prices, bid_volumes = zip(*range_of_ticks_to_draw[index][1])
        ask_prices, ask_volumes = zip(*range_of_ticks_to_draw[index][2])
        # scaling here volume 500.000 to one pixel
        bid_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        # Pixel range
        min_pixel_vertical = 10
        #max_pixel_vertical = 1664
        # Calculate scaling factor
        scaling_factor = (max_pixel_vertical - min_pixel_vertical) / (max_price - min_price)
        # Map each price to its pixel value
        bid_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in bid_prices]
        ask_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in ask_prices]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        bid_volume_pixels = list(zip(bid_pixels, bid_volumes_pixels))
        ask_volume_pixels = list(zip(ask_pixels, ask_volumes_pixels))
        top_left_coordinate_left = canvas_with_left - max_volume_pixel -1
        # drawing volumes on the left
        [canvas.create_rectangle(top_left_coordinate_left, price_bid_pixel, top_left_coordinate_left + volume_bid_pixel, price_bid_pixel+10, fill="green") for price_bid_pixel, volume_bid_pixel in bid_volume_pixels] #bids
        [canvas.create_rectangle(top_left_coordinate_left, price_ask_pixel, top_left_coordinate_left + volume_ask_pixel, price_ask_pixel+10, fill="red") for price_ask_pixel, volume_ask_pixel in ask_volume_pixels] #asks
        canvas_with_left = top_left_coordinate_left
    root.after(20, lambda: draw_dom_data_on_canvas(canvas, dom_data_full, end_tick_bar_to_draw + 1))

root = tk.Tk()
root.title("EUR USD deep of the market")
root.state('zoomed') # Maximize the window
canvas = tk.Canvas(root, bg='gray')
canvas.pack(fill='both', expand=True)  # Fill and expand in both directions
end_tick_bar_to_draw = 1
draw_dom_data_on_canvas(canvas, scope_data, end_tick_bar_to_draw)
    
root.mainloop()







# scope_data[1][0] # index
# scope_data[1][1] # bid values
# scope_data[1][2] # ask values
# scope_data[1][3] # total bid ask values

# coord 1,2,3,4
# 1,2 is top-left corner coordinate (left-right, top-down)
# 3,4 is bottom-right corner coordinate (left-right, top-down) 
# canvas.create_rectangle(50, 150, 150, 150, fill="blue")

