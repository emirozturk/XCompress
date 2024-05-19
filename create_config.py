import os
import json


def get_config_input():
    config = {}

    print("Enter configuration parameters:")

    config["name"] = input("Name: ")
    config["executable_path"] = input("Executable Path \n Enter just the name if it exists on path, full path otherwise: ")
    config["input_file_param"] = input("Input File Parameter\n (If input file needs special prefix or suffix)\n [Press Enter for default]: ")
    config["input_file_param"]+="{input_file}"
    config["output_file_param"] = input("Output File Parameter\n (If output file needs special prefix or suffix\n if algorithm gives output to console, use stdout keyword)\n [Press Enter for default]: ")
    if config["output_file_param"]!="stdout": config["output_file_param"]+="{output_file}"
    config["compression_params"] = input("Compression Parameters (comma-separated)\n For example, if algorithm uses -c for compression and -k for keeping files -c,-k can be entered: ").split(",")
    config["decompression_params"] = input("Decompression Parameters (comma-separated) \n For example, if algorithm uses -d for decompression and -k for keeping files -d,-k can be entered: ").split(",")
    config["extension"] = input("Extension \n If stdout is used, extension parameter will be used as compressed file extension:")

    return config

def save_config_to_file(config, folder_path):
    name = config["name"]
    file_path = os.path.join(folder_path, f"{name}.json")

    with open(file_path, "w") as file:
        json.dump(config, file, indent=4)

    print(f"Configurations saved to {file_path}")


def create_config_param(name,executable_path,input_file_param,output_file_param,compression_params,decompression_params,extension):
    config = {}
    config["name"] = name
    config["executable_path"] = executable_path
    config["input_file_param"] = input_file_param
    config["input_file_param"]+="{input_file}"
    config["output_file_param"] = output_file_param
    if config["output_file_param"]!="stdout": config["output_file_param"]+="{output_file}"
    config["compression_params"] = compression_params
    config["decompression_params"] = decompression_params
    config["extension"] = extension

    return config

def create_config():
    config = get_config_input()
    save_config_to_file(config, os.path.join(os.path.dirname(__file__),"compression_configs"))
    input("Press any key to continue...")  
    return