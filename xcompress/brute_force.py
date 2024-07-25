from .compress import compress_with_config
from .util import clear_screen, load_configs, get_config
import os


def print_menu(selected_row, options):
    """
    Prints a menu for selecting compression modes.

    Args:
        selected_row (int): The index of the currently selected row.
        options (List[str]): List of compression mode options.
    """
    clear_screen()
    print("Select Compression Mode:")
    for idx, option in enumerate(options):
        if idx == 0:
            if selected_row == 0:
                print(
                    "\033[1;32m->\033[0m", "\033[1;32m", "Back to main menu", "\033[0m"
                )
            else:
                print("\033[32m   ", "Back to main menu", "\033[0m")
        elif selected_row == idx:
            print("\033[1;32m->\033[0m", "\033[1;32m", option, "\033[0m")
        else:
            print("\033[32m   ", option, "\033[0m")


def brute_force_param(filename, out_folder, delete_except_minimum=False):
    """
    Performs brute-force compression using all available configurations and selects the one with the minimum compressed size.

    Args:
        filename (str): Path to the input file.
        out_folder (str): Directory where output files are stored.
        output_filename (str): Path for the output file.
        delete_except_minimum (bool, optional): If True, deletes all files except the one with the minimum compressed size.
    """
    result_list = []
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)

    for config_file in configs:
        name = config_file["name"]
        try:
            extension = config_file["extension"]
            print(f"Trying {name}...")
            out_file_name = os.path.join(
                out_folder, f"{os.path.basename(filename)}.{extension}"
            )
            output_file, compression_time_ns = compress_with_config(
                config_file, filename, out_file_name
            )
            compressed_size = os.path.getsize(output_file)
            result_list.append(
                {
                    "name": name,
                    "compressed_size": compressed_size,
                    "output_file": output_file,
                }
            )
        except Exception as e:
            print(f"Error getting results for {name}. Error message:", e)

    # Determine the compression configuration with the minimum size
    min_size_name = min(result_list, key=lambda x: x["compressed_size"])["name"]

    if delete_except_minimum:
        for result in result_list:
            if result["name"] != min_size_name:
                os.remove(result["output_file"])

    selected_config = get_config(configs, min_size_name)

    output, _ = compress_with_config(selected_config, filename, "")

    print("\033[1mSelected compression algorithm:\033[0m", min_size_name)
    print("\033[1mInput filename:\033[0m", filename)
    print("\033[1mOutput filename:\033[0m", output)

    print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    input("Press any key to exit")
    return selected_config


def brute_force_compression():
    """
    Prompts the user for input and output file details, and performs brute-force compression using all available configurations and selects the one with the minimum compressed size.
    """
    filename = input("\033[1mEnter input filename: \033[0m")
    output_filename = input("\033[1mEnter output filename (optional): \033[0m")
    delete_except_minimum = input("\033[1mKeep only minimum sized file([Y]/n) \033[0m")

    delete_except_minimum = delete_except_minimum.lower() in ["y", ""]

    return brute_force_param(
        filename, os.path.dirname(__file__), output_filename, delete_except_minimum
    )
