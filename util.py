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