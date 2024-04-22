import readchar
from compress import compress_with_config
from util import clear_screen
from util import load_configs
from util import get_config
import os

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


def brute_force(filename,configs,out_folder):
    result_list = []
    for config_file in configs:
        name = config_file["name"]            
        extension = config_file["extension"]
        if not os.path.exists(os.path.join(out_folder,name)):
            os.makedirs(os.path.join(out_folder,name))
        out_file_name = os.path.join(out_folder,name,f"{os.path.basename(filename)}.{extension}")
        output_file,compression_time_ns = compress_with_config(config_file,filename,out_file_name)
        compressed_size = os.path.getsize(output_file)
        result_list.append({name,compressed_size})
        min_size_name = lambda result_list: min(result_list, key=lambda x: x["compressed_size"])["name"]
    return min_size_name
    

def brute_force_compression():
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    filename = input("\033[1mEnter input filename: \033[0m")
    output_filename = input("\033[1mEnter output filename (optional): \033[0m")
    selected_algorithm = brute_force(filename,configs,os.path.dirname(__file__))
    selected_config = get_config(configs,selected_algorithm)
    print("\033[1mSelected compression algorithm:\033[0m", )
    print("\033[1mInput filename:\033[0m", filename)
    print("\033[1mOutput filename:\033[0m", output_filename)
    clear_screen()
    output,_ = compress_with_config(selected_config,filename,output_filename)
    print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    input("Press any key to return to menu")
    return