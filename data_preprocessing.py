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
