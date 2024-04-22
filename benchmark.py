import readchar
from compress import compress_with_config
from decompress import decompress_with_config
from util import clear_screen
from util import load_configs
import os 

def print_menu(options, selected_rows, config_count):
    clear_screen()
    print(f"{config_count} configuration file(s) found.\n")
    print("Select Compression Algorithm(s):")
    print("\033[1;32m->\033[0m", "\033[1;32m", "Back to main menu", "\033[0m" if 0 in selected_rows else "   Back to main menu")
    for idx, option in enumerate(options):
        if idx in selected_rows:
            print("\033[1;32m->\033[0m", "\033[1m", option['name'], "\033[0m")
        else:
            print("   ", option['name'])
    print("Accept")

def select_config(prev_configs=None):
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    if prev_configs == None:
        selected_configs = set()
    current_row = 0
    continue_selection = True
    while continue_selection:
        print_menu(configs, selected_configs, len(configs))
        key = readchar.readkey()
        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < len(configs):
            current_row += 1
        elif key == ' ':
            if current_row == 0:
                return None
            elif current_row in selected_configs:
                selected_configs.remove(current_row)
            else:
                selected_configs.add(current_row)
        elif key == '\r' or key == '\n':
            if current_row == 0:
                return None            
            elif current_row == len(configs)+2: #config len + back + accept
                return selected_configs
            continue


def select_benchmark_type():
    menu_options = ["back to menu", "compress", "compress-decompress"]
    selected_index = 0

    def display_menu():
        nonlocal selected_index
        for i, option in enumerate(menu_options):
            if i == selected_index:
                print("\033[1m{}\033[0m".format(option))
            else:
                print(option)

    display_menu()
    
    while True:
        key = readchar.readkey()
        if key == readchar.key.ENTER:
            if selected_index == 0:
                print("Back to menu")
                return None
            elif selected_index == 1:
                print("Compress")
                return "compress"
            elif selected_index == 2:
                print("Compress-decompress")
                return "compress-decompress"
        elif key == readchar.key.UP:
            selected_index = (selected_index - 1) % 3
            display_menu()
        elif key == readchar.key.DOWN:
            selected_index = (selected_index + 1) % 3
            display_menu()


def benchmark(output_to_file=False):
    while True:
        selected_configs = select_config()
        if selected_configs == None:
            return        
        benchmark_type = select_benchmark_type()        
        if benchmark_type == None:
            print("No benchmark selected.")
        else:
            for config in selected_configs:
                filename = input("\033[1mEnter input filename: \033[0m")
                output_filename = input("\033[1mEnter output filename (optional): \033[0m")

                print("\033[1mSelected compression algorithm:\033[0m", config['name'])
                print("\033[1mInput filename:\033[0m", filename)
                print("\033[1mOutput filename:\033[0m", output_filename)
                clear_screen()
                result_list = []
                if benchmark_type == "compress":
                    output_file,compression_time_ns = compress_with_config(config,filename,output_filename)
                    file_size = os.path.getsize(filename)
                    compressed_size = os.path.getsize(output_file)
                    result_list.append({"filename":filename,
                                        "name":config["name"],
                                        "file_size":file_size,
                                        "compressed_size":compressed_size,
                                        "compression_time_ns":compression_time_ns})
                if benchmark_type == "compress-decompress":
                    output_file,compression_time_ns = compress_with_config(config,filename,output_filename)
                    file_size = os.path.getsize(filename)
                    if output_file != "":            
                        _,decompression_time_ns = decompress_with_config(config,output_file)
                    compressed_size = os.path.getsize(output_file)
                    result_list.append({"filename":filename,
                                        "name":config["name"],
                                        "file_size":file_size,
                                        "compressed_size":compressed_size,
                                        "compression_time_ns":compression_time_ns,
                                        "decompression_time_ns":decompression_time_ns})
                    
            if output_to_file:
                with open("benchmark_results.txt", "w") as file:
                    for result in result_list:
                        file.write("Filename: {}\n".format(result["filename"]))
                        file.write("Name: {}\n".format(result["name"]))
                        file.write("File Size: {}\n".format(result["file_size"]))
                        file.write("Compressed Size: {}\n".format(result["compressed_size"]))
                        file.write("Compression Time (ns): {}\n".format(result["compression_time_ns"]))
                        file.write("Decompression Time (ns): {}\n".format(result["decompression_time_ns"]))
                        file.write("\n")
            else:
                for result in result_list:
                    print("Filename:", result["filename"])
                    print("Name:", result["name"])
                    print("File Size:", result["file_size"])
                    print("Compressed Size:", result["compressed_size"])
                    print("Compression Time (ns):", result["compression_time_ns"])
                    print("Decompression Time (ns):", result["decompression_time_ns"])
                    print()