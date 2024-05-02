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


def brute_force(filename, configs, out_folder, delete_except_minimum=False):
    result_list = []
    for config_file in configs:
        name = config_file["name"]            
        try:
            extension = config_file["extension"]
            out_file_name = os.path.join(out_folder, name, f"{os.path.basename(filename)}.{extension}")
            output_file, compression_time_ns = compress_with_config(config_file, filename, out_file_name)
            compressed_size = os.path.getsize(output_file)
            result_list.append({"name": name, "compressed_size": compressed_size, "output_file": output_file})
        except Exception as e:
            print(f"Error getting results for {name}. Error message:",e)    
    min_size_name = min(result_list, key=lambda x: x["compressed_size"])["name"]
        
    if delete_except_minimum:
        for result in result_list:
            if result["name"] != min_size_name:
                os.remove(result["output_file"])
    
    return min_size_name


def brute_force_compression():
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    filename = input("\033[1mEnter input filename: \033[0m")
    output_filename = input("\033[1mEnter output filename (optional): \033[0m")
    delete_except_minimum = input("\033[1mKeep only minimum sized file([Y]/n) \033[0m")
    if delete_except_minimum == "Y" or delete_except_minimum == "y" or delete_except_minimum == "":
        delete_except_minimum = True
    else:
        delete_except_minimum = False
    selected_algorithm = brute_force(filename,configs,os.path.dirname(__file__),delete_except_minimum)
    selected_config = get_config(configs,selected_algorithm)
    print("\033[1mSelected compression algorithm:\033[0m", )
    print("\033[1mInput filename:\033[0m", filename)
    print("\033[1mOutput filename:\033[0m", output_filename)
    clear_screen()
    output,_ = compress_with_config(selected_config,filename,output_filename)
    print(f"Compression completed successfully. Filename is \033[1m{output}\033[0m")
    input("Press any key to return to menu")
    return