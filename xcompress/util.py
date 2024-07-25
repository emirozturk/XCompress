import platform
import os
import json


def clear_screen():
    """
    Clears the terminal screen.

    The method used to clear the screen depends on the operating system:
    - Windows: Uses 'cls' command.
    - Other systems (e.g., Unix-based): Uses 'clear' command.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def load_configs(folder_path):
    """
    Loads configuration files from a specified folder.

    Args:
        folder_path (str): The path to the folder containing configuration files.

    Returns:
        list of dict: A list of configuration dictionaries loaded from JSON files.
    """
    configs = []
    folder_path = os.path.join(os.path.dirname(__file__), folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                config = json.load(file)
                configs.append(config)
    return configs


def get_config(configs, selected_algorithm):
    """
    Retrieves a configuration dictionary based on the selected algorithm name.

    Args:
        configs (list of dict): List of configuration dictionaries.
        selected_algorithm (str): The name of the desired algorithm to find.

    Returns:
        dict or None: The configuration dictionary for the selected algorithm, or None if not found.
    """
    for config in configs:
        if config["name"] == selected_algorithm:
            return config
    return None


def count_unique_symbols(file_path):
    """
    Counts the number of unique symbols in a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The number of unique symbols in the file.
    """
    with open(file_path, "r") as file:
        text = file.read()
        unique_symbols = set(text)
        return len(unique_symbols)


def round_to_class(file_size_bytes):
    """
    Rounds the file size to a specific class based on byte ranges.

    Args:
        file_size_bytes (int): The size of the file in bytes.

    Returns:
        str: A string representing the rounded size class ("1kb", "10kb", "100kb", "1mb", "10mb", or "100mb").
    """
    if file_size_bytes < 1050:  # For 1025 issue
        return "1kb"
    elif file_size_bytes < 10500:  # For 10241 issue
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
    """
    Bins the unique symbol count (USC) value into a multiple of 50.
    To use USC as a feature to train ai model, selected features must have limited values. If USC is given raw, accuracy decreases.
    To prevent this, USC values have been divided into groups of 50.

    Args:
        usc_value (int): The unique symbol count value.

    Returns:
        int: The binned unique symbol count.
    """
    bin_size = 50
    return int((usc_value // bin_size) * bin_size)


def get_file_size(file_path):
    """
    Gets the size of a file in bytes.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.
    """
    size = os.path.getsize(file_path)
    return size
