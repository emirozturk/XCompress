import readchar
from compress import compress_with_config
from util import clear_screen
from util import load_configs
from util import get_config
from llm_model import detect_algorithm

def print_menu(selected_row,options):
    clear_screen()
    print("Select Compression Mode:")
    for idx, option in enumerate(options):
        if idx == 0:
            if selected_row == 0:
                print("\033[1;32m->\033[0m", "\033[1;32m", "Back to main menu", "\033[0m")
            else:
                print("\033[32m   ", "Back to main menu", "\033[0m")
        elif selected_row == idx:
            print("\033[1;32m->\033[0m", "\033[1;32m", option[idx], "\033[0m")
        else:
            print("\033[32m   ", option[idx], "\033[0m")


def model_compression():
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)

    mode_list = ["Speed","Compression","Balanced"]
    current_row = 0
    mode = 1
    while True:
        print_menu(current_row,mode_list)
        key = readchar.readkey()
        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < 3:
            current_row += 1
        elif key == '\r' or key == '\n':
            if current_row == 0:
                return
            elif current_row == 1:
                mode = 1  # Speed
                break
            elif current_row == 2:
                mode = 2  # Compression
                break
            elif current_row == 3:
                mode = 3  # Balanced 
                break
        
    filename = input("\033[1mEnter input filename: \033[0m")
    output_filename = input("\033[1mEnter output filename (optional): \033[0m")
    selected_algorithm = detect_algorithm(filename,mode)
    selected_config = get_config(configs,selected_algorithm)
    print("\033[1mSelected compression algorithm:\033[0m", )
    print("\033[1mInput filename:\033[0m", filename)
    print("\033[1mOutput filename:\033[0m", output_filename)
    clear_screen()
    output,_ = compress_with_config(selected_config,filename,output_filename)
    print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    input("Press any key to return to menu")
    return