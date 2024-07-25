import readchar
from .compress import compress_with_config
from .util import clear_screen, load_configs
import os

def print_menu(options, selected_row, config_count):
    """
    Displays a menu for selecting a compression algorithm from a list of available configurations.

    Args:
        options (list of dict): List of available compression configurations. Each configuration is a dictionary with a "name" key.
        selected_row (int): The index of the currently selected menu item to highlight.
        config_count (int): The total number of configuration files found.
    """
    clear_screen()
    print(f"{config_count-1} configuration file(s) found.\n")
    print("Select Compression Algorithm:")
    for idx, option in enumerate(options):
        if idx == 0:
            if selected_row == 0:
                print(
                    "\033[1;32m->\033[0m", "\033[1;32m", "Back to the menu", "\033[0m"
                )
            else:
                print("\033[32m   ", "Back to the menu", "\033[0m")
        elif idx == selected_row:
            print("\033[1;32m->\033[0m", "\033[1m", option["name"], "\033[0m")
        else:
            print("   ", option["name"])


def select_compression_param(selected_config_name, filename, output_filename):
    """
    Selects a specific compression configuration and applies it to the input file.

    Args:
        selected_config_name (str): The name of the selected compression configuration.
        filename (str): The path to the file to compress.
        output_filename (str): The path to save the compressed file (optional; defaults to input filename with an appropriate extension if not provided).
    """
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        configs_folder = "compression_configs"
        configs = load_configs(configs_folder)
        selected_config = [x for x in configs if x["name"] == selected_config_name][0]
        print("\033[1mSelected compression algorithm:\033[0m", selected_config)
        print("\033[1mInput filename:\033[0m", filename)
        print("\033[1mOutput filename:\033[0m", output_filename)
        clear_screen()
        
        output = compress_with_config(selected_config, filename, output_filename)
        print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    except Exception as e:
        print(f"Error during compression: {e}")
        return "", 0


def select_compression():
    """
    Allows the user to select a compression algorithm from a menu and apply it to a specified file.

    The function loads available compression configurations from a folder, displays them in a menu, and allows the user to navigate and select one.
    After selection, it prompts the user for input and output filenames and performs the compression.
    """
    current_row = 0
    while True:
        configs_folder = "compression_configs"
        configs = load_configs(configs_folder)
        print_menu(configs, current_row, len(configs))
        key = readchar.readkey()

        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < len(configs) - 1:
            current_row += 1
        elif key == "\r" or key == "\n":
            if current_row == 0:
                return
            else:
                filename = input("\033[1mEnter input filename: \033[0m")
                output_filename = input(
                    "\033[1mEnter output filename (optional): \033[0m"
                )
                select_compression_param(
                    configs[current_row]["name"], filename, output_filename
                )
                input("Press any key to return to menu")
                return

        elif key.lower() == "q":
            break
