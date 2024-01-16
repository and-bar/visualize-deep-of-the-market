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
import numpy as np

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
full_data_of_ticks = sorted(load_pickle_files(directory), key=lambda x: x[0]) # sort of tickes based on index

# with purpose of quicker visualization from tick data will be deleted small volumes for beter visual representation
boundry_of_volume_for_deletion = 500000
scope_data = [[sublist[0], [pair for pair in sublist[1] if pair[1] >= boundry_of_volume_for_deletion], [pair for pair in sublist[2] if pair[1] >= boundry_of_volume_for_deletion], sublist[3]] for sublist in full_data_of_ticks]

# scope_data = full_data_of_ticks

def draw_dom_data_on_canvas (canvas, dom_data_full, end_tick_bar_to_draw):
    """draw dom data on the canvas"""
    # logic of how many ticks can be visualized on width of canvas
    if canvas.winfo_width() == 1:
        maximum_with_canvas = 1027
        max_pixel_vertical = 980
    else:
        maximum_with_canvas = canvas.winfo_width() - 100
        max_pixel_vertical = canvas.winfo_height() - 20 # -20 here for allowing drawing on the canvas minimum bid presented
    
    # getting info how many tick can fir into canvas with
    
    # scaling here volume n000000 to one pixel
    one_pixel_equeal_n_volume = 500000

    bottom_right_coord_vertical_tick_separator_line_bottom = max_pixel_vertical + 20
    space_between_volume_bars = 2
    height_of_volume_bar_in_pixels = 10
    canvas_with_left = maximum_with_canvas #3840
    dom_data = dom_data_full[:end_tick_bar_to_draw]
    lenght_ofdom_data_elements = len(dom_data)
    n_tick = lenght_ofdom_data_elements - 1
    while ((canvas_with_left > 0) and (n_tick >= 0)):
        bid_prices, bid_volumes = zip(*dom_data[n_tick][1])
        ask_prices, ask_volumes = zip(*dom_data[n_tick][2])
        bid_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        canvas_with_left -= max_volume_pixel - space_between_volume_bars
        # can not draw to the left
        if canvas_with_left - max_volume_pixel <= 0:
            break
        n_tick -= 1

    start_index_tick_data = n_tick+1
    # find max and min prices among all ticks
    range_of_ticks_to_draw = dom_data[start_index_tick_data:lenght_ofdom_data_elements]
    max_price = max([pair[0] for sublist in [tick_data[2]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    min_price = min([pair[0] for sublist in [tick_data[1]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    # draw all tick data on canvas
    canvas.delete("all")
    canvas_with_left = maximum_with_canvas #3840
    for index in range(len(range_of_ticks_to_draw)-1, -1, -1):
        bid_prices, bid_volumes = zip(*range_of_ticks_to_draw[index][1])
        ask_prices, ask_volumes = zip(*range_of_ticks_to_draw[index][2])
        bid_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        # Pixel range
        min_pixel_vertical = 10
        # Calculate scaling factor
        scaling_factor = (max_pixel_vertical - min_pixel_vertical) / (max_price - min_price)
        # Map each price to its pixel value
        bid_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in bid_prices]
        ask_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) for price in ask_prices]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        bid_volume_pixels = list(zip(bid_pixels, bid_volumes_pixels))
        ask_volume_pixels = list(zip(ask_pixels, ask_volumes_pixels))
        top_left_coordinate_left = canvas_with_left - max_volume_pixel - space_between_volume_bars
        # drawing volumes on the
        [canvas.create_rectangle(top_left_coordinate_left, price_bid_pixel, top_left_coordinate_left + volume_bid_pixel, price_bid_pixel+height_of_volume_bar_in_pixels, fill="green") for price_bid_pixel, volume_bid_pixel in bid_volume_pixels] #bids
        [canvas.create_rectangle(top_left_coordinate_left, price_ask_pixel, top_left_coordinate_left + volume_ask_pixel, price_ask_pixel+height_of_volume_bar_in_pixels, fill="red") for price_ask_pixel, volume_ask_pixel in ask_volume_pixels] #asks
        # draw vertical line separation between ticks
        canvas.create_rectangle(top_left_coordinate_left, 0, top_left_coordinate_left, bottom_right_coord_vertical_tick_separator_line_bottom, fill= "black")
        canvas_with_left = top_left_coordinate_left
    
    # draw horizontal prices lines each 0.0001 and 0.00005 price level
    whole_range_of_0_00001 = np.arange(min_price, max_price, 0.00001)
    nested_list  = [[level, round(level+0.00005, 5)] for level in whole_range_of_0_00001 if ( int(("{:.5f}".format(level))[-1]) / 5) == 1]
    list_price_levels = [element for pair in nested_list for element in pair]
    level_line_prices_pixels = [int(max_pixel_vertical - (price - min_price) * scaling_factor) + height_of_volume_bar_in_pixels for price in list_price_levels]
    [canvas.create_rectangle(0, price_level, maximum_with_canvas + 20, price_level, fill="black") for price_level in level_line_prices_pixels]
    list_price_levels_plus_pixel_levels = list(zip(list_price_levels, level_line_prices_pixels))
    [canvas.create_text(maximum_with_canvas + 60, level_line_prices_pixels, text= "{:.5f}".format(round(price, 5)), fill="black", font=('Helvetica', '15', 'bold italic')) for price, level_line_prices_pixels in list_price_levels_plus_pixel_levels]
    
    root.after(10, lambda: draw_dom_data_on_canvas(canvas, dom_data_full, end_tick_bar_to_draw + 3))

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

