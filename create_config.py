import os
import json

def get_config_input():
    config = {}

    print("Enter configuration parameters:")

    config["name"] = input("Name: ")
    config["executable_path"] = input("Executable Path: ")
    config["input_file_param"] = input("Input File Parameter: ")
    config["output_file_param"] = input("Output File Parameter: ")
    config["compression_params"] = input("Compression Parameters (comma-separated): ").split(",")
    config["decompression_params"] = input("Decompression Parameters (comma-separated): ").split(",")
    config["extension"] = input("Extension: ")

    return config

def save_config_to_file(config, folder_path):
    name = config["name"]
    file_path = os.path.join(folder_path, f"{name}.json")

    with open(file_path, "w") as file:
        json.dump(config, file, indent=4)

    print(f"Configurations saved to {file_path}")

def create_config():
    config = get_config_input()
    folder_path = input("Enter folder path to save the configuration file: ")
    save_config_to_file(config, folder_path)
    input("Press any key to continue...")  
    return