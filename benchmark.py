import readchar
from compress import compress_with_config
from decompress import decompress_with_config
from util import clear_screen, load_configs,get_config
import matplotlib.pyplot as plt
import os

configs = []


def print_menu(options, selected_rows, config_count, current_row):
    clear_screen()
    print(f"{config_count} configuration file(s) found.\n")
    print("Use spacebar to select algorithms, selected will be shown in green")
    print("Select Compression Algorithm(s):")
    
    # Print "Back to main menu" option
    if current_row == 0:
        print("\033[1;32m->\033[0m", "\033[1;32m", "Back to main menu", "\033[0m")
    else:
        print("   ", "Back to main menu")
    
    # Print the rest of the options
    for idx, option in enumerate(options):
        if idx in selected_rows:
            if current_row == idx + 1:  # Shift by 1 to account for "Back to main menu" option
                print("\033[1;32m->\033[0m", "\033[1;32m", option['name'], "\033[0m")
            else:
                print("\033[1;32m", option['name'], "\033[0m")
        else:
            if current_row == idx + 1:  # Shift by 1 to account for "Back to main menu" option
                print("\033[1;32m->\033[0m", option['name'])
            else:
                print("   ", option['name'])
    
    # Print the "Accept" option
    if len(options) + 1 in selected_rows:  # Adjusted index for the Accept option
        if current_row == len(options) + 1:  # Shift by 1 to account for "Back to main menu" option
            print("\033[1;32m->\033[0m", "\033[1;32m", "Accept", "\033[0m")
        else:
            print("\033[1;32m", "Accept", "\033[0m")
    else:
        if current_row == len(options) + 1:  # Shift by 1 to account for "Back to main menu" option
            print("\033[1;32m->\033[0m", "Accept")
        else:
            print("   ", "Accept")


def select_config(prev_configs=None):
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
        elif key == readchar.key.DOWN and current_row < len(configs)+1:
            current_row += 1
        elif key == '\r' or key == '\n':
            if current_row == 0:
                return None
            if current_row == len(configs) + 1:
                return selected_configs
        elif key == ' ':
            if current_row != len(configs)+2:
                if current_row == 0:
                    return None
                elif current_row-1 in selected_configs:
                    selected_configs.remove(current_row-1)
                else:
                    selected_configs.add(current_row-1)


def display_select_benchmark_menu(menu_options, selected_index):
    clear_screen()
    print("Select benchmark type:")
    for i, option in enumerate(menu_options):
        if i == selected_index:
            print("\033[1;32m-> {}\033[0m".format(option))
        else:
            print("   {}".format(option))
         
            
def select_benchmark_type():
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


def plot_results(results):
    algorithms = list(set([result['name'] for result in results]))

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    # Plot compressed size comparison
    ax1.bar(algorithms, [result['compressed_size'] for result in results], color='skyblue')
    ax1.set_title('Compressed Size Comparison')
    ax1.set_ylabel('Compressed Size (bytes)')

    # Plot compression time comparison
    ax2.bar(algorithms, [result['compression_time_ns'] for result in results], color='lightgreen')
    ax2.set_title('Compression Time Comparison')
    ax2.set_ylabel('Compression Time (ns)')

    # Plot decompression time comparison if available
    decompression_times = [result['decompression_time_ns'] for result in results if 'decompression_time_ns' in result]
    if decompression_times:
        ax3.bar(algorithms, decompression_times, color='salmon')
        ax3.set_title('Decompression Time Comparison')
        ax3.set_ylabel('Decompression Time (ns)')
    else:
        ax3.axis('off')  # Hide decompression time comparison if not available

    # Adjust layout
    plt.subplots_adjust(hspace=0.5)

    # Save plots to files
    fig.savefig("results_compressed_size.png")
    fig.savefig("results_compression_time.png")
    fig.savefig("results_decompression_time.png")


def benchmark_param(selected_config_names,benchmark_type,filename,output_filename,output_to_file=False, output_plots=False):
    all_results = []
    configs_folder = "compression_configs"
    configs = load_configs(configs_folder)
    selected_configs = [get_config(configs,x) for x in selected_config_names]
    result_list = []
    for config in selected_configs:
        print("\033[1mSelected compression algorithm:\033[0m", config['name'])
        print("\033[1mInput filename:\033[0m", filename)
        print("\033[1mOutput filename:\033[0m", output_filename)
        if benchmark_type == "compress":
            output_file, compression_time_ns = compress_with_config(config, filename, output_filename)
            file_size = os.path.getsize(filename)
            compressed_size = os.path.getsize(output_file)
            result_list.append({"filename": filename,
                                "name": configs[config]["name"],
                                "file_size": file_size,
                                "compressed_size": compressed_size,
                                "compression_time_ns": compression_time_ns})
        if benchmark_type == "compress_decompress":
            output_file, compression_time_ns = compress_with_config(config, filename, output_filename)
            file_size = os.path.getsize(filename)
            if output_file != "":            
                _, decompression_time_ns = decompress_with_config(config, output_file)
            compressed_size = os.path.getsize(output_file)
            result_list.append({"filename": filename,
                                "name": config["name"],
                                "file_size": file_size,
                                "compressed_size": compressed_size,
                                "compression_time_ns": compression_time_ns,
                                "decompression_time_ns": decompression_time_ns})

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
    
    if output_plots:
        plot_results(result_list)


def read_boolean_input(prompt):
    print(prompt)
    while True:
        key = readchar.readkey()
        if key.lower() == 'y':
            return True
        elif key.lower() == 'n':
            return False


def benchmark():
    selected_configs = select_config()
    if selected_configs == None:
        return        
    benchmark_type = select_benchmark_type()        
    if benchmark_type == None:
        print("No benchmark selected.")
    else:
        filename = input("\033[1mEnter input filename: \033[0m")
        output_filename = input("\033[1mEnter output filename (optional): \033[0m")
        output_to_file = read_boolean_input("Output to file? (y/n): ")
        output_plots = read_boolean_input("Output plots? (y/n): ")
        benchmark_param([x["name"] for x in selected_configs],benchmark_type,filename,output_filename, output_to_file, output_plots)
