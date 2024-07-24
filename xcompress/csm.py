import readchar
from compress import compress_with_config
from util import clear_screen, load_configs, get_config
from llm_model import detect_algorithm

def print_menu(selected_row, options):
    """
    Prints the menu options, highlighting the selected option.
    
    Args:
        selected_row (int): Index of the currently selected option.
        options (list of str): List of menu options to display.
    """
    clear_screen()
    print("Select Compression Mode:")
    for idx, option in enumerate(options):
        if selected_row == idx:
            print("\033[1;32m->\033[0m", "\033[1;32m", option, "\033[0m")
        else:
            print("\033[37m   ", option, "\033[0m")  # Set to white


def model_compression_param(filename, mode, output_filename):
    """
    Executes compression based on the selected algorithm and mode.
    
    Args:
        filename (str): The input file to compress.
        mode (str): The compression mode.
        output_filename (str): The name of the output file.
    """
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    
    # Detect the algorithm based on filename and mode
    selected_algorithm = detect_algorithm(filename, mode.lower().replace(" ", "-"))
    selected_config = get_config(configs, selected_algorithm)
    
    if selected_config is None:
        print(f"Error: No configuration found for algorithm {selected_algorithm}.")
        input("Press any key to return to menu")
        return

    print("\033[1mSelected compression algorithm:\033[0m", selected_algorithm)
    print("\033[1mInput filename:\033[0m", filename)
    print("\033[1mOutput filename:\033[0m", output_filename)
    clear_screen()
    
    try:
        output, _ = compress_with_config(selected_config, filename, output_filename)
        print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    except Exception as e:
        print(f"Error during compression: {e}")
    
    input("Press any key to return to menu")


def model_compression():
    """
    Displays the model compression menu and handles user selection.
    """
    mode_list = ["Back to main menu", "Fast Compression", "Fast Decompression", "Best Compression"]
    current_row = 0  # Start from the first option

    while True:
        print_menu(current_row, mode_list)
        key = readchar.readkey()
        
        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < len(mode_list) - 1:
            current_row += 1
        elif key in {'\r', '\n'}:
            if current_row == 0:
                return
            mode = current_row  # Mode is directly mapped from the row index
            
            filename = input("\033[1mEnter input filename: \033[0m").strip()
            output_filename = input("\033[1mEnter output filename (optional): \033[0m").strip()

            if not filename:
                print("Error: Input filename cannot be empty.")
                continue

            model_compression_param(filename, mode_list[mode], output_filename)