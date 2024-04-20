"""Concatenate pickle files to one file for ueach subfolder of main folder"""

import os
import pickle

def get_subfolders(directory):
    """Returns a list of names of all subfolders in the given directory."""
    subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
    return subfolders


def load_files_save_them_in_unique_file(directory, subfolder_name):
    """Load and concatenate lists from all pickle files in the given directory."""
    concatenated_list = []
    for filename in os.listdir(directory + subfolder_name):
        if filename.endswith('.pickle_list'):
            filepath = os.path.join(directory + subfolder_name, filename)
            try:
                with open(filepath, 'rb') as file:
                    data = pickle.load(file)
                    if isinstance(data, list):
                        concatenated_list.extend(data)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    with open(directory + subfolder_name + ".pickle_list", 'wb') as file:
        pickle.dump(concatenated_list, file)

directory_path = 'C:/Temp/dom request data/modified/need for modification/'
subfolder_list = get_subfolders(directory_path)
for subfolder_name in subfolder_list:
    load_files_save_them_in_unique_file(directory_path, subfolder_name)




""" deleting from pickle file all tick elements of the list where at least one side bid or ask do not have any price level """

import os
import pickle
directory = "C:/Temp/dom request data/modified/need for modification"
directory_modified = "C:/Temp/dom request data/modified/need for modification/0 levels deleted"
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'rb') as file:
                dom_data = pickle.load(file)
            print(filepath)
            lenght_original_file = len(dom_data)
            print(f"len of dom data before processing: {lenght_original_file}")
            new_dom_data = [tick for tick in dom_data if ( tick[1] != [])]
            new_dom_data = [tick for tick in new_dom_data if ( tick[2] != [])]
            lenght_new_data = len(new_dom_data)
            print(f"len of dom after deleting emty ticks: {lenght_new_data}")
            print(f"TICKS DELETED: {lenght_original_file - lenght_new_data}")
            name, extension = os.path.splitext(filename)            
            if lenght_original_file != lenght_new_data:
                filename_new = directory_modified + "/" + filename
                with open(filename_new, 'wb') as write_file:
                    pickle.dump(new_dom_data, write_file)
        except Exception as e:
            print(f"Error loading {filename}: {e}")



"""
opening each pickle file, loking for difference in price between market price and farest price of each side, bid and ask,
to say, deleting all leveles volumes that are far more than 0.0012 points from market prices, same for bids and for asks
this is done for beter visualisation of the volumes flow, as market prices will not be squized to single line because of 
level prices that are to far from the market

"""

import os
import pickle
directory = "C:/Temp/dom request data/test"
directory_modified = "C:/Temp/dom request data/test/modified/"
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'rb') as file:
                full_data_of_ticks_1 = pickle.load(file)
        except Exception as e:
            print(f"Error loading {filename}: {e}  was reading file {filepath}")

        full_data_of_ticks =[]
        for tick in full_data_of_ticks_1:
            if tick[1] == []:
                print(f"next tick has [] value: {tick}")
            else:
                full_data_of_ticks.append(tick)

        for _ in range(5):
            full_data_of_ticks = [[tick[0], tick[1][:-1], tick[2], tick[3]] if (tick[1][0][0] - tick[1][-1][0]) > 0.0012 else [tick[0], tick[1], tick[2], tick[3]]  for tick in full_data_of_ticks]
            full_data_of_ticks = [[tick[0], tick[1], tick[2][:-1], tick[3]] if (tick[2][-1][0] - tick[2][0][0]) > 0.0012 else [tick[0], tick[1], tick[2], tick[3]]  for tick in full_data_of_ticks]
            
        file_name_path = directory_modified + filename

        try:
            with open(file_name_path, 'wb') as write_file:
                pickle.dump(full_data_of_ticks, write_file)
        except Exception as e:
            print(f"Error loading {filename}: {e}  was writing file {file_name_path}")
        




"""
Create one second timeframe OHLCV candle charts save them to png

"""
import pandas as pd
import mplfinance as mpf
import pandas

# Sample DataFrame with OHLCV data
df = pd.read_pickle("pandas_df_1_second_OHLCV_eurusd_11-2019.pkl")
df.index = df.index.tz_localize(None)

seconds_in_chart = 2000
start= 0
end= seconds_in_chart
while True:
    data = df[start:end]
    date_time_first_tick = str(df.index[start])
    date_time_first_tick = date_time_first_tick.replace(':', '-')
    image_file_name = date_time_first_tick + '_startcandlestick_chart.png'
    mpf.plot(data, type='candle', volume=True, title='EUR USD', style='yahoo', savefig= image_file_name, figscale=1.5, figratio=(5, 1), tight_layout=True, datetime_format='%b %d %H:%M:%S')
    start +=seconds_in_chart
    end +=seconds_in_chart
    if end > df.shape[0]:
        break


"""
Create pandas dataframe forming 1 second OLHCV rows based on the data from tick of dom
"""
import pickle
import pandas as pd
import datetime

filepath = 'C:\Temp\dom request data\cleaned-dom-eurusd-01-2020.pickle_list'
with open(filepath, 'rb') as file:
    current_data = pickle.load(file)

# Define the column names
columns = ['open', 'high', 'low', 'close', 'volume']
# Create an empty DataFrame with these columns
df_second_candlestick = pd.DataFrame(columns=columns)
df_second_candlestick['volume'] = df_second_candlestick['volume'].astype(float)

# running through dom list and forming 1 second dataframe OLHCV
for tick in current_data:
    time_of_tick_with_miliseconds = tick[0]
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
    bid_of_last_tick = tick[1][0][0]
    total_volume_bid_ask_of_last_tick = tick[3][1] + tick[3][0]
    #print(f"{time_of_tick}   {bid_of_last_tick}   {total_volume_bid_ask_of_last_tick}")

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

print(df_second_candlestick.shape)
df_second_candlestick.to_pickle("C:\Temp\dom request data\pandas_df_1_second_OHLCV_eurusd_01-2020.pkl")



"""
sorting all ticks by time in pickle files
"""

import os
import pickle
directory = "C:/Temp/dom request data"
directory_modified = "C:/Temp/dom request data/ordered by indices"
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):
        
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'rb') as file:
            dom_data = pickle.load(file)
        
        dom_data = sorted(dom_data, key=lambda x: x[0]) # sort of tickes based on index
        
        filename_new = directory_modified + "/" + filename
        with open(filename_new, 'wb') as write_file:
            pickle.dump(dom_data, write_file)


"""
concatenate pickle files
"""
import os, pickle

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

directory = 'C:/Temp/dom request data/01-2020'
full_data_of_ticks = load_pickle_files(directory)

filename_new = 'C:/Temp/dom request data/cleaned-dom-eurusd-01-2020.pickle_list'
with open(filename_new, 'wb') as write_file:
            pickle.dump(full_data_of_ticks, write_file)


