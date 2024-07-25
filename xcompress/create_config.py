import os
import json


def get_config_input():
    """
    Prompts the user for configuration parameters and returns a dictionary containing the inputs.

    Returns:
        dict: A dictionary with configuration parameters.
    """
    config = {}

    print("Enter configuration parameters:")

    config["name"] = input("Name: ").strip()
    config["executable_path"] = input(
        "Executable Path \n Enter just the name if it exists on path, full path otherwise: "
    ).strip()
    config["input_file_param"] = input(
        "Input File Parameter\n (If input file needs special prefix or suffix)\n [Press Enter for default]: "
    ).strip()
    config["input_file_param"] += " {input_file}"
    config["output_file_param"] = input(
        "Output File Parameter\n (If output file needs special prefix or suffix\n if algorithm gives output to console, use stdout keyword)\n [Press Enter for default]: "
    ).strip()
    if config["output_file_param"] != "stdout":
        config["output_file_param"] += " {output_file}"
    config["compression_params"] = [
        x.strip()
        for x in input(
            "Compression Parameters (comma-separated)\n For example, if algorithm uses -c for compression and -k for keeping files -c,-k can be entered: "
        ).split(",")
    ]
    config["decompression_params"] = [
        x.strip()
        for x in input(
            "Decompression Parameters (comma-separated) \n For example, if algorithm uses -d for decompression and -k for keeping files -d,-k can be entered: "
        ).split(",")
    ]
    config["extension"] = input(
        "Extension \n If stdout is used, extension parameter will be used as compressed file extension: "
    ).strip()

    return config


def save_config_to_file(config, folder_path):
    """
    Saves the configuration dictionary to a JSON file in the specified folder.

    Args:
        config (dict): The configuration dictionary.
        folder_path (str): The path to the folder where the config file will be saved (compression_configs preferred).
    """
    name = config["name"]
    file_path = os.path.join(folder_path, f"{name}.json")

    with open(file_path, "w") as file:
        json.dump(config, file, indent=4)

    print(f"Configurations saved to {file_path}")


def create_config_param(
    name,
    executable_path,
    input_file_param,
    output_file_param,
    compression_params,
    decompression_params,
    extension,
):
    """
    Creates a configuration dictionary from given parameters.

    Args:
        name (str): The name of the configuration.
        executable_path (str): Path to the executable.
        input_file_param (str): Input file parameter.
        output_file_param (str): Output file parameter.
        compression_params (list): List of compression parameters.
        decompression_params (list): List of decompression parameters.
        extension (str): File extension.

    Returns:
        dict: A configuration dictionary.
    """
    config = {
        "name": name,
        "executable_path": executable_path,
        "input_file_param": input_file_param + "{input_file}",
        "output_file_param": (
            output_file_param + "{output_file}"
            if output_file_param != "stdout"
            else "stdout"
        ),
        "compression_params": compression_params,
        "decompression_params": decompression_params,
        "extension": extension,
    }

    return config


def create_config():
    """
    Collects configuration inputs from the user, creates a configuration dictionary,
    and saves it to a file in the 'compression_configs' folder.
    """
    config = get_config_input()
    save_config_to_file(
        config, os.path.join(os.path.dirname(__file__), "compression_configs")
    )
    input("Press any key to continue...")
