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