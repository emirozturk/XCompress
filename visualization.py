import json
import matplotlib.pyplot as plt
import os
from util import clear_screen
import readchar


def print_menu():
    clear_screen()
    file_paths_input = input("Enter the JSON file paths (space-separated): ")
    file_paths = [path.strip() for path in file_paths_input.split(" ")]
    return file_paths

def read_results_from_files(file_paths):
    all_results = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                results = json.load(file)
                all_results.extend(results)
        else:
            print(f"File not found: {file_path}")
    return all_results


def visualization_param(results):
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
    plt.show()


def visualization():
    file_paths = print_menu()

    if file_paths:
        results = read_results_from_files(file_paths)
        if results:
            visualization_param(results)
        else:
            print("No valid results to display.")
    else:
        print("No file paths provided.")