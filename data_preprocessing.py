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

directory_path = 'C:/Temp/deep of the market data in pickles EURUSD/all periods/'
subfolder_list = get_subfolders(directory_path)
for subfolder_name in subfolder_list:
    load_files_save_them_in_unique_file(directory_path, subfolder_name)




""" deleting from pickle file all tick elements of the list where at least one side bid or ask do not have any price level """

import os
import pickle
directory = "C:/Temp/dom request data"
directory_modified = "C:/Temp/dom request data/modified"
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'rb') as file:
                dom_data = pickle.load(file)
            print(filepath)
            lenght_original_file = len(dom_data)
            print(f"len of dom data before processing: {lenght_original_file}")
            new_dom_data = [tick for tick in dom_data if ( tick[1] != [] or tick[2] != [])]
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
directory = "C:/Temp/dom request data"
directory_modified = "C:/Temp/dom request data/modified/"
for filename in os.listdir(directory):
    if filename.endswith('.pickle_list'):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'rb') as file:
                full_data_of_ticks = pickle.load(file)
            
            for _ in range(5):
                full_data_of_ticks = [[tick[0], tick[1][:-1], tick[2], tick[3]] if (tick[1][0][0] - tick[1][-1][0]) > 0.0012 else [tick[0], tick[1], tick[2], tick[3]]  for tick in full_data_of_ticks]
                full_data_of_ticks = [[tick[0], tick[1], tick[2][:-1], tick[3]] if (tick[2][-1][0] - tick[2][0][0]) > 0.0012 else [tick[0], tick[1], tick[2], tick[3]]  for tick in full_data_of_ticks]
            
            file_name_path = directory_modified + filename
            with open(file_name_path, 'wb') as write_file:
                pickle.dump(full_data_of_ticks, write_file)
        
        except Exception as e:
            print(f"Error loading {filename}: {e}")
