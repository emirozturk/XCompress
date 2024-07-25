import readchar
from compress import compress_with_config
from decompress import decompress_with_config
from util import clear_screen, load_configs, get_config
import json
import os
from visualization import visualization_param

configs = []


def print_menu(options, selected_rows, config_count, current_row):
    """
    Prints the menu for selecting compression algorithms.

    Args:
        options (List[Dict[str, str]]): List of defined compression algorithms with configuration files.
        selected_rows (Set[int]): Set of indices of selected options.
        config_count (int): Total number of configuration options.
        current_row (int): The currently selected row in the menu.
    """
    clear_screen()
    print(f"{config_count} configuration file(s) found.\n")
    print("Use spacebar to select algorithms; selected ones will be shown in green")
    print("Select Compression Algorithm(s):")

    # Print "Back to main menu" option
    if current_row == 0:
        print("\033[1;32m->\033[0m", "\033[1;32m", "Back to main menu", "\033[0m")
    else:
        print("   ", "Back to main menu")

    # Print the rest of the options
    for idx, option in enumerate(options):
        if idx in selected_rows:
            if (
                current_row == idx + 1
            ):  # Shift by 1 to account for "Back to main menu" option
                print("\033[1;32m->\033[0m", "\033[1;32m", option["name"], "\033[0m")
            else:
                print("\033[1;32m", option["name"], "\033[0m")
        else:
            if (
                current_row == idx + 1
            ):  # Shift by 1 to account for "Back to main menu" option
                print("\033[1;32m->\033[0m", option["name"])
            else:
                print("   ", option["name"])

    # Print the "Accept" option
    if len(options) + 1 in selected_rows:  # Adjusted index for the Accept option
        if (
            current_row == len(options) + 1
        ):  # Shift by 1 to account for "Back to main menu" option
            print("\033[1;32m->\033[0m", "\033[1;32m", "Accept", "\033[0m")
        else:
            print("\033[1;32m", "Accept", "\033[0m")
    else:
        if (
            current_row == len(options) + 1
        ):  # Shift by 1 to account for "Back to main menu" option
            print("\033[1;32m->\033[0m", "Accept")
        else:
            print("   ", "Accept")


def select_config(prev_configs=None):
    """
    Allows the user to select compression configurations from a menu.

    Args:
        prev_configs (Set[int], optional): Previously selected configurations.

    Returns:
        Set[int]: Set of indices of selected configurations.
    """
    configs_folder = "compression_configs"
    global configs
    configs = load_configs(configs_folder)
    if prev_configs is None:
        selected_configs = set()
    else:
        selected_configs = prev_configs
    current_row = 0
    continue_selection = True
    while continue_selection:
        print_menu(configs, selected_configs, len(configs), current_row)
        key = readchar.readkey()
        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < len(configs) + 1:
            current_row += 1
        elif key in ("\r", "\n"):
            if current_row == 0:
                return None
            if current_row == len(configs) + 1:
                return selected_configs
        elif key == " ":
            if current_row != len(configs) + 2:
                if current_row == 0:
                    return None
                elif current_row - 1 in selected_configs:
                    selected_configs.remove(current_row - 1)
                else:
                    selected_configs.add(current_row - 1)


def display_select_benchmark_menu(menu_options, selected_index):
    """
    Displays the benchmark type selection menu.

    Args:
        menu_options (List[str]): List of benchmark type options.
        selected_index (int): Index of the currently selected option.
    """
    clear_screen()
    print("Select benchmark type:")
    for i, option in enumerate(menu_options):
        if i == selected_index:
            print("\033[1;32m-> {}\033[0m".format(option))
        else:
            print("   {}".format(option))


def select_benchmark_type():
    """
    Allows the user to select a benchmark type from a menu.

    Returns:
        str: The selected benchmark type ("compress" or "compress_decompress"), or None if canceled.
    """
    menu_options = ["Back to menu", "Compress", "Compress-decompress"]
    selected_index = 0

    display_select_benchmark_menu(menu_options, selected_index)

    while True:
        key = readchar.readkey()
        if key == readchar.key.ENTER:
            if selected_index == 0:
                return None
            elif selected_index == 1:
                return "compress"
            elif selected_index == 2:
                return "compress_decompress"
        elif key == readchar.key.UP:
            selected_index = (selected_index - 1) % 3
            display_select_benchmark_menu(menu_options, selected_index)
        elif key == readchar.key.DOWN:
            selected_index = (selected_index + 1) % 3
            display_select_benchmark_menu(menu_options, selected_index)


def benchmark_param(
    selected_config_names,
    benchmark_type,
    filename,
    output_filename,
    output_to_file=False,
    output_plots=False,
):
    """
    Benchmarks the selected compression configurations and either outputs results to a file or displays them.

    Args:
        selected_config_names (List[str]): List of names of selected configurations (compression methods).
        benchmark_type (str): Type of benchmark ("compress" or "compress_decompress").
        filename (str): Path to the input file.
        output_filename (str): Path to the output file.
        output_to_file (bool, optional): If True, results are saved to a file.
        output_plots (bool, optional): If True, plots are generated and displayed.
    """
    try:
        configs_folder = "compression_configs"
        configs = load_configs(configs_folder)
        selected_configs = [get_config(configs, x) for x in selected_config_names]
        result_list = []
        for config in selected_configs:
            print("\033[1mSelected compression algorithm:\033[0m", config["name"])
            print("\033[1mInput filename:\033[0m", filename)
            print("\033[1mOutput filename:\033[0m", output_filename)
            if benchmark_type == "compress":
                output_file, compression_time_ns = compress_with_config(
                    config, filename, output_filename
                )
                file_size = os.path.getsize(filename)
                compressed_size = os.path.getsize(output_file)
                result_list.append(
                    {
                        "filename": filename,
                        "name": config["name"],
                        "file_size": file_size,
                        "compressed_size": compressed_size,
                        "compression_time_ns": compression_time_ns,
                    }
                )
            elif benchmark_type == "compress_decompress":
                output_file, compression_time_ns = compress_with_config(
                    config, filename, output_filename
                )
                file_size = os.path.getsize(filename)
                if output_file != "":
                    _, decompression_time_ns = decompress_with_config(config, output_file)
                compressed_size = os.path.getsize(output_file)
                result_list.append(
                    {
                        "filename": filename,
                        "name": config["name"],
                        "file_size": file_size,
                        "compressed_size": compressed_size,
                        "compression_time_ns": compression_time_ns,
                        "decompression_time_ns": decompression_time_ns,
                    }
                )

        if output_to_file:
            with open("benchmark_results.json", "w") as file:
                json.dump(result_list, file, indent=4)
        else:
            print("Results:")
            for result in result_list:
                print("Filename:", result["filename"])
                print("Name:", result["name"])
                print("File Size:", result["file_size"])
                print("Compressed Size:", result["compressed_size"])
                print("Compression Time (ns):", result["compression_time_ns"])
                print(
                    "Decompression Time (ns):", result.get("decompression_time_ns", "N/A")
                )
                print()

        if output_plots:
            visualization_param(result_list)
    except Exception as e:
        print(f"Error: {e}")

def read_boolean_input(prompt):
    """
    Reads a boolean input from the user.

    Args:
        prompt (str): The prompt message to display.

    Returns:
        bool: True if 'y' is entered, False if 'n' is entered.
    """
    print(prompt)
    while True:
        key = readchar.readkey()
        if key.lower() == "y":
            return True
        elif key.lower() == "n":
            return False


def benchmark():
    """
    Main function for running benchmarks. Allows the user to select configurations, benchmark type, and output options.
    """
    selected_configs = select_config()
    if selected_configs is None:
        return
    benchmark_type = select_benchmark_type()
    if benchmark_type is None:
        print("No benchmark selected.")
    else:
        filename = input("\033[1mEnter input filename: \033[0m")
        output_filename = input("\033[1mEnter output filename (optional): \033[0m")
        output_to_file = read_boolean_input("Output to file? (y/n): ")
        output_plots = read_boolean_input("Output plots? (y/n): ")
        benchmark_param(
            [x["name"] for x in selected_configs],
            benchmark_type,
            filename,
            output_filename,
            output_to_file,
            output_plots,
        )
