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
            print(filename)
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    data = pickle.load(file)
                    if isinstance(data, list):
                        concatenated_list.extend(data)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return concatenated_list

def get_canvas_size_for_drawing_volumes(canvas):
    """Get canvas size that will be used for maximum boundaries drawing of tick volumes"""
    global root
    if canvas.winfo_width() == 1:
        return root.winfo_screenwidth() - 80, root.winfo_screenheight() - 120
    else:
        return canvas.winfo_width() - 80, canvas.winfo_height() - 140
    
def get_number_of_ticks_that_will_fit_on_canvas (dom_data_full, maximum_with_canvas, one_pixel_equeal_n_volume, space_between_volume_bars, end_tick_bar_to_draw):
    "get number of ticks that will be drawn on canvas"
    #canvas_with_left = maximum_with_canvas #3840
    dom_data = dom_data_full[:end_tick_bar_to_draw]
    n_tick = len(dom_data) - 1
    #while ((maximum_with_canvas > 0) and (n_tick >= 0)):
    while True:
        _, bid_volumes = zip(*dom_data[n_tick][1])
        _, ask_volumes = zip(*dom_data[n_tick][2])
        bid_volumes_pixels = [int(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [int(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        maximum_with_canvas -= max_volume_pixel + space_between_volume_bars
        if ((maximum_with_canvas - max_volume_pixel) < 0) or (n_tick == 0): # can not draw to the left
            break
        n_tick -= 1
    return dom_data, n_tick #+1

def draw_one_frame_on_the_canvas (maximum_height_canvas, dom_data, start_index_tick_data, maximum_with_canvas, one_pixel_equeal_n_volume, space_between_volume_bars, height_of_volume_bar_in_pixels):
    """draw one frame on the canvas"""
    global canvas, date_of_first_tick_of_full_data, date_of_last_tick_of_full_data
    bottom_right_coord_vertical_tick_separator_line_bottom = maximum_height_canvas + 20
    range_of_ticks_to_draw = dom_data[start_index_tick_data:]
    max_price = max([pair[0] for sublist in [tick_data[2]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    min_price = min([pair[0] for sublist in [tick_data[1]  for tick_data in range_of_ticks_to_draw] for pair in sublist])
    canvas.delete("all")
    canvas_with_left = maximum_with_canvas
    # - - - - - preprocessing of data for drawing of total volumes and volume levels lines start
    bid_total_volumes_of_tick = [tick_data[3][0]  for tick_data in range_of_ticks_to_draw]
    ask_total_volumes_of_tick = [tick_data[3][1]  for tick_data in range_of_ticks_to_draw]
    max_bid_ask_total_volumes_of_tick = max(max(bid_total_volumes_of_tick), max(ask_total_volumes_of_tick))
    height_in_pixels_of_total_bids = [int(volume / max_bid_ask_total_volumes_of_tick * 100) for volume in bid_total_volumes_of_tick]
    height_in_pixels_of_total_asks = [int(volume / max_bid_ask_total_volumes_of_tick * 100) for volume in ask_total_volumes_of_tick]
    #drawing horizontal volumes lines
    total_volumes_price_levels = np.arange(0,max_bid_ask_total_volumes_of_tick, 10000000)
    total_volumes_price_levels = np.append(total_volumes_price_levels[1:-1], max_bid_ask_total_volumes_of_tick)
    total_volume_levels_lines_pixels = [int(level/max_bid_ask_total_volumes_of_tick*100) for level in total_volumes_price_levels]
    total_level_lines_texts_pixel = zip(total_volumes_price_levels, total_volume_levels_lines_pixels)
    # draw lines of total volumes levels
    [canvas.create_rectangle(0, bottom_right_coord_vertical_tick_separator_line_bottom+120-level, maximum_with_canvas, bottom_right_coord_vertical_tick_separator_line_bottom+120-level) for level in total_volume_levels_lines_pixels]
    [canvas.create_text(maximum_with_canvas + 40, bottom_right_coord_vertical_tick_separator_line_bottom+120-level_line_volumes_pixels, text= f"{text:,}".replace(",", "."), fill="black", font=('Helvetica', '10', 'bold italic')) for text, level_line_volumes_pixels in total_level_lines_texts_pixel]
    # - - - - - preprocessing of data for drawing of total volumes  and volume levels lines end
    for index in range(len(range_of_ticks_to_draw)-1, -1, -1):
        bid_prices, bid_volumes = zip(*range_of_ticks_to_draw[index][1])
        ask_prices, ask_volumes = zip(*range_of_ticks_to_draw[index][2])
        bid_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in bid_volumes]
        ask_volumes_pixels = [round(element / one_pixel_equeal_n_volume) for element in ask_volumes]
        # Pixel range
        min_pixel_vertical = 10
        # Calculate scaling factor
        scaling_factor = (maximum_height_canvas - min_pixel_vertical) / (max_price - min_price)
        # Map each price to its pixel value
        bid_pixels = [int(maximum_height_canvas - (price - min_price) * scaling_factor) for price in bid_prices]
        ask_pixels = [int(maximum_height_canvas - (price - min_price) * scaling_factor) for price in ask_prices]
        max_volume_pixel = max(max(bid_volumes_pixels), max(ask_volumes_pixels))
        bid_volume_pixels = list(zip(bid_pixels, bid_volumes_pixels))
        ask_volume_pixels = list(zip(ask_pixels, ask_volumes_pixels))
        top_left_coordinate_left = canvas_with_left - max_volume_pixel - space_between_volume_bars
        # draw vertical line separation between ticks
        canvas.create_rectangle(top_left_coordinate_left, 0, top_left_coordinate_left, bottom_right_coord_vertical_tick_separator_line_bottom + 120, fill= "black", outline= "gray45")
        # drawing volumes on the canvas
        [canvas.create_rectangle(top_left_coordinate_left, price_bid_pixel, top_left_coordinate_left + volume_bid_pixel, price_bid_pixel+height_of_volume_bar_in_pixels, fill="lime green", outline="dark green") for price_bid_pixel, volume_bid_pixel in bid_volume_pixels] #bids
        [canvas.create_rectangle(top_left_coordinate_left, price_ask_pixel, top_left_coordinate_left + volume_ask_pixel, price_ask_pixel+height_of_volume_bar_in_pixels, fill="red", outline="red4") for price_ask_pixel, volume_ask_pixel in ask_volume_pixels] #asks
        # drawing total volumes on the canvas
        canvas.create_rectangle(top_left_coordinate_left+2, bottom_right_coord_vertical_tick_separator_line_bottom+120, top_left_coordinate_left+5, bottom_right_coord_vertical_tick_separator_line_bottom + 120 - height_in_pixels_of_total_bids[index], fill="green") #total bid
        canvas.create_rectangle(top_left_coordinate_left+6, bottom_right_coord_vertical_tick_separator_line_bottom+120, top_left_coordinate_left+9, bottom_right_coord_vertical_tick_separator_line_bottom + 120 - height_in_pixels_of_total_asks[index], fill="red") #total ask
        canvas_with_left = top_left_coordinate_left
    # draw horizontal prices lines each 0.0001 and 0.00005 price level
    whole_range_of_0_00001 = np.arange(min_price, max_price, 0.00001)
    nested_list  = [[level, level+0.00005] for level in whole_range_of_0_00001 if ( int(("{:.5f}".format(level))[-1]) / 5) == 1]
    list_price_levels = [element for pair in nested_list for element in pair]
    if (list_price_levels[0]-min_price > 0.00005):
        list_price_levels.append(list_price_levels[0]-0.00005)
    else:
        list_price_levels.append(min_price)
    level_line_prices_pixels = [int(maximum_height_canvas - (price - min_price) * scaling_factor) + height_of_volume_bar_in_pixels for price in list_price_levels]
    [canvas.create_rectangle(0, price_level, maximum_with_canvas, price_level, fill="black") for price_level in level_line_prices_pixels]
    list_price_levels_plus_pixel_levels = list(zip(list_price_levels, level_line_prices_pixels))
    [canvas.create_text(maximum_with_canvas + 40, level_line_prices_pixels, text= "{:.5f}".format(round(price, 5)), fill="black", font=('Helvetica', '15', 'bold italic')) for price, level_line_prices_pixels in list_price_levels_plus_pixel_levels]
    # update text info of the label on the bottom
    date_time_of_last_tick = f"{range_of_ticks_to_draw[-1][0].year}:{range_of_ticks_to_draw[-1][0].month}:{range_of_ticks_to_draw[-1][0].day} - {range_of_ticks_to_draw[-1][0].hour}:{range_of_ticks_to_draw[-1][0].minute}:{range_of_ticks_to_draw[-1][0].second}      "
    max_bid_label_text = f"{max(bid_total_volumes_of_tick):,}".replace(",", ".")
    max_ask_label_text = f"{max(ask_total_volumes_of_tick):,}".replace(",", ".")
    label.config(text= "First tick: " + date_of_first_tick_of_full_data + "     Last tick: " + date_of_last_tick_of_full_data + "     Current tick: " + date_time_of_last_tick + f"           MAX BID {max_bid_label_text} |  MAX ASK: {max_ask_label_text}") 

def draw_dom_data_on_canvas (canvas, dom_data_full, end_tick_bar_to_draw, one_pixel_equeal_n_volume):
    """draw dom data on the canvas"""
    global pause_drawing_on_the_canvas, end_tick_bar_to_draw_dynamic
    maximum_with_canvas, maximum_height_canvas = get_canvas_size_for_drawing_volumes(canvas)
    space_between_volume_bars = 2
    height_of_volume_bar_in_pixels = 10
    dom_data, start_index_tick_data = get_number_of_ticks_that_will_fit_on_canvas (dom_data_full, maximum_with_canvas, one_pixel_equeal_n_volume, space_between_volume_bars, end_tick_bar_to_draw)
    draw_one_frame_on_the_canvas (maximum_height_canvas, dom_data, start_index_tick_data, maximum_with_canvas, one_pixel_equeal_n_volume, space_between_volume_bars, height_of_volume_bar_in_pixels)
    if pause_drawing_on_the_canvas == False:
        step_of_next_shift = 20
        end_tick_bar_to_draw_dynamic += step_of_next_shift
        # in next line you can control how many next ticks will be drawn on the canvas: end_tick_bar_to_draw + ##
        root.after(10, lambda: draw_dom_data_on_canvas(canvas, dom_data_full, end_tick_bar_to_draw + step_of_next_shift, one_pixel_equeal_n_volume))

def toggle_pause_drawing_on_the_canvas(dom_data_full):
    global pause_drawing_on_the_canvas
    pause_drawing_on_the_canvas = not pause_drawing_on_the_canvas
    if pause_drawing_on_the_canvas == False:
        draw_dom_data_on_canvas(canvas, dom_data_full, end_tick_bar_to_draw_dynamic, one_pixel_equeal_n_volume)

directory = 'C:/Temp/dom request data/test'
# full_data_of_ticks = sorted(load_pickle_files(directory), key=lambda x: x[0]) # sort of tickes based on index
full_data_of_ticks = load_pickle_files(directory)

# with purpose of quicker visualization from tick data will be deleted small volumes for beter visual representation
boundry_of_volume_for_deletion = 50000
one_pixel_equeal_n_volume = 1000000 # scaling here volume n000000 to one pixel
end_tick_bar_to_draw = 1
end_tick_bar_to_draw_dynamic = 1
scope_data = [[sublist[0], [pair for pair in sublist[1] if pair[1] >= boundry_of_volume_for_deletion], [pair for pair in sublist[2] if pair[1] >= boundry_of_volume_for_deletion], sublist[3]] for sublist in full_data_of_ticks]
pause_drawing_on_the_canvas = False
root = tk.Tk()
root.title("EUR USD deep of the market. Volume scale: 1 pixel = " + f"{one_pixel_equeal_n_volume:,}".replace(",", ".") + " USD.")
root.state('zoomed') # Maximize the window

# Configure the grid layout
root.grid_columnconfigure(0, weight=1)  # Make the canvas column expandable
root.grid_columnconfigure(1, weight=0)  # Fixed width column for the text widget
root.grid_rowconfigure(0, weight=1)     # Make the canvas row expandable
root.grid_rowconfigure(1, weight=0)     # Fixed height row for the button and text widget

canvas = tk.Canvas(root, bg='gray40')
canvas.grid(row=0, column=0, columnspan=2, sticky='nsew')  # Span two columns

pause_button = tk.Button(root, text="Pause", command=lambda: toggle_pause_drawing_on_the_canvas(scope_data) )
pause_button.grid(row=1, column=0, sticky='nw')

# Create and place the Text widget (memo)
date_of_first_tick_of_full_data = f"{full_data_of_ticks[0][0].year}:{full_data_of_ticks[0][0].month}:{full_data_of_ticks[0][0].day} - {full_data_of_ticks[0][0].hour}:{full_data_of_ticks[0][0].minute}:{full_data_of_ticks[0][0].second}"
date_of_last_tick_of_full_data = f"{full_data_of_ticks[-1][0].year}:{full_data_of_ticks[-1][0].month}:{full_data_of_ticks[-1][0].day} - {full_data_of_ticks[-1][0].hour}:{full_data_of_ticks[-1][0].minute}:{full_data_of_ticks[-1][0].second}"
label = tk.Label(root, text="", anchor="w", fg="red")
label.grid(row=1, column=1, sticky='nw')

draw_dom_data_on_canvas(canvas, scope_data, end_tick_bar_to_draw, one_pixel_equeal_n_volume)
root.mainloop()

# scope_data[1][0] # index
# scope_data[1][1] # bid values
# scope_data[1][2] # ask values
# scope_data[1][3] # total bid ask values

# coord 1,2,3,4
# 1,2 is top-left corner coordinate (left-right, top-down)
# 3,4 is bottom-right corner coordinate (left-right, top-down) 
# canvas.create_rectangle(50, 150, 150, 150, fill="blue")

