import json
import plotly.graph_objects as go
import os
from util import clear_screen
import readchar


def print_menu():
    """
    Prompts the user to enter JSON file paths and returns a list of file paths.

    Returns:
        list of str: A list of file paths entered by the user, split by spaces.
    """
    clear_screen()
    file_paths_input = input("Enter the JSON file paths (space-separated): ")
    file_paths = [path.strip() for path in file_paths_input.split(" ")]
    return file_paths

def read_results_from_files(file_paths):
    """
    Reads and combines results from multiple JSON files.

    Args:
        file_paths (list of str): A list of file paths to JSON files.

    Returns:
        list of dict: A combined list of results from all specified JSON files.
    """
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
    """
    Generates and displays a bar chart visualizing compression benchmark results.

    Args:
        results (list of dict): A list of benchmark results containing metrics like compressed size,
                                compression time, and optionally decompression time.
    """
    algorithms = list(set([result['name'] for result in results]))

    # Create traces for compressed size
    compressed_size_trace = go.Bar(
        x=algorithms,
        y=[result['compressed_size'] for result in results],
        name='Compressed Size',
        marker_color='skyblue'
    )

    # Create traces for compression time
    compression_time_trace = go.Bar(
        x=algorithms,
        y=[result['compression_time_ns'] for result in results],
        name='Compression Time',
        marker_color='lightgreen'
    )

    # Create traces for decompression time if available
    decompression_times = [result['decompression_time_ns'] for result in results if 'decompression_time_ns' in result]
    if decompression_times:
        decompression_time_trace = go.Bar(
            x=algorithms,
            y=decompression_times,
            name='Decompression Time',
            marker_color='salmon'
        )

    # Create subplots
    fig = go.Figure()

    fig.add_trace(compressed_size_trace)
    fig.add_trace(compression_time_trace)
    if decompression_times:
        fig.add_trace(decompression_time_trace)

    fig.update_layout(
        title='Compression Benchmark Results',
        barmode='group',
        xaxis_title='Algorithms',
        yaxis_title='Values',
        legend_title='Metrics',
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Compressed Size",
                        "method": "update",
                        "args": [{"visible": [True, False, False]}]
                    },
                    {
                        "label": "Compression Time",
                        "method": "update",
                        "args": [{"visible": [False, True, False]}]
                    },
                    {
                        "label": "Decompression Time",
                        "method": "update",
                        "args": [{"visible": [False, False, True]}]
                    },
                    {
                        "label": "All",
                        "method": "update",
                        "args": [{"visible": [True, True, bool(decompression_times)]}]
                    },
                ],
                "direction": "down",
                "showactive": True,
            }
        ]
    )

    fig.show()

    # Save plots to files
    fig.write_image("results_compressed_size.png")
    fig.write_image("results_compression_time.png")
    fig.write_image("results_decompression_time.png")


def visualization():
    """
    Main function to handle the visualization process:
    - Prompts the user for file paths.
    - Reads results from the specified files.
    - Generates and displays a bar chart visualizing the benchmark results.
    """
    file_paths = print_menu()

    if file_paths:
        results = read_results_from_files(file_paths)
        if results:
            visualization_param(results)
        else:
            print("No valid results to display.")
    else:
        print("No file paths provided.")