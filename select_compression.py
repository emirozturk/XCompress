import readchar
from compress import compress_with_config
from util import clear_screen
from util import load_configs


def print_menu(options, selected_row,config_count):
    clear_screen()
    print(f"{config_count-1} configuration file(s) found.\n")
    print("Select Compression Algorithm:")
    for idx, option in enumerate(options):
        if idx == 0:
            if selected_row == 0:
                print("\033[1;32m->\033[0m", "\033[1;32m", "Back to the menu", "\033[0m")
            else:
                print("\033[32m   ", "Back to the menu", "\033[0m")
        elif idx == selected_row:
            print("\033[1;32m->\033[0m", "\033[1m", option['name'], "\033[0m")
        else:
            print("   ", option['name'])


def select_compression():
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    current_row = 0
    while True:
        print_menu(configs, current_row,len(configs))
        key = readchar.readkey()

        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < len(configs) - 1:
            current_row += 1
        elif key == '\r' or key == '\n':
            if current_row == 0:
                return
            else:
                selected_config = configs[current_row]
                filename = input("\033[1mEnter input filename: \033[0m")
                output_filename = input("\033[1mEnter output filename (optional): \033[0m")

                print("\033[1mSelected compression algorithm:\033[0m", selected_config['name'])
                print("\033[1mInput filename:\033[0m", filename)
                print("\033[1mOutput filename:\033[0m", output_filename)
                clear_screen()
                output = compress_with_config(selected_config,filename,output_filename)
                print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
                input("Press any key to return to menu")
                return
        elif key.lower() == 'q':
            break