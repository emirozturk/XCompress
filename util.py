import platform
import os
import json


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        

def load_configs(folder_path):
    configs = []
    folder_path = os.path.join(os.path.dirname(__file__),folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                config = json.load(file)
                configs.append(config)
    return configs


def get_config(configs, selected_algorithm):
    for config in configs:
        if config['name'] == selected_algorithm:
            return config
    return None


def count_unique_symbols(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        unique_symbols = set(text)
        return len(unique_symbols)


def round_to_class(file_size_bytes):
    if file_size_bytes < 1050: #For 1025 issue
        return "1kb" 
    elif file_size_bytes < 10500: #For 10241 issue
        return "10kb"
    elif file_size_bytes < 105000:
        return "100kb" 
    elif file_size_bytes < 1050000:
        return "1mb"
    elif file_size_bytes < 10500000:
        return "10mb"  
    else:
        return "100mb"  
    
    
def bin_usc(usc_value):
    bin_size = 50
    return int((usc_value // bin_size) * bin_size)


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size