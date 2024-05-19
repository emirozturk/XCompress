import readchar
import sys
from select_compression import select_compression,select_compression_param
from bcm import model_compression,model_compression_param
from benchmark import benchmark,benchmark_param
from brute_force import brute_force_compression,brute_force_param
from create_config import create_config,create_config_param
from util import clear_screen
import argparse
import readchar
import sys

menu = ["Select compression algorithm",
        "Use BCM (AI) for auto algorithm selection",
        "Find best compression using brute force",
        "Get benchmark results for specific file",
        "Create config for custom compression algorithm"]


def print_menu(selected_row):
    clear_screen()
    print('\n\033[1mXCompress\033[0m is a tool for selecting the best text compression algorithm for a given input.')
    print('You can choose any algorithm you want, determine the best compression or fastest compression algorithm with BCM AI,')
    print('and select the best compression algorithm with brute force.\n')
    print("Please make a selection:\n")
    for idx, row in enumerate(menu):
        if idx == selected_row:
            print("\033[1;32m->\033[0m", "\033[1;32m", row, "\033[0m")
        else:
            print("   ", row)
    print("Press q to quit")
    

def main():
    parser = argparse.ArgumentParser(description="Compression Tool")
    
    subparsers = parser.add_subparsers(dest="command")

    # Select Compression
    parser_select_compression = subparsers.add_parser("select_compression")
    parser_select_compression.add_argument("algorithm_name")
    parser_select_compression.add_argument("input_filename")
    parser_select_compression.add_argument("--output_filename", default=None)

    # Model Compression
    parser_model_compression = subparsers.add_parser("model_compression")
    parser_model_compression.add_argument("mode", choices=["speed", "best-compression", "balanced"])
    parser_model_compression.add_argument("input_filename")
    parser_model_compression.add_argument("--output_filename", default=None)

    # Brute Force Compression
    parser_brute_force = subparsers.add_parser("brute_force_compression")
    parser_brute_force.add_argument("input_filename")
    parser_brute_force.add_argument("output_filename")
    parser_brute_force.add_argument("delete_except_minimum", type=bool)

    # Benchmark
    parser_benchmark = subparsers.add_parser("benchmark")
    parser_benchmark.add_argument("selected_config_names", nargs='+')
    parser_benchmark.add_argument("benchmark_type", choices=["compress", "compress-decompress"])
    parser_benchmark.add_argument("output_to_file", type=bool)
    parser_benchmark.add_argument("output_plots", type=bool)

    # Create Config
    parser_create_config = subparsers.add_parser("create_config")
    parser_create_config.add_argument("name")
    parser_create_config.add_argument("executable_path")
    parser_create_config.add_argument("input_file_param")
    parser_create_config.add_argument("output_file_param")
    parser_create_config.add_argument("compression_params")
    parser_create_config.add_argument("decompression_params")
    parser_create_config.add_argument("extension")

    args = parser.parse_args()

    if args.command is None:
        # No command provided, show the menu
        current_row = 0
        print_menu(current_row)
        while True:
            key = readchar.readkey()
            if key == readchar.key.UP and current_row > 0:
                current_row -= 1
            elif key == readchar.key.DOWN and current_row < 4:
                current_row += 1
            elif key == '\r' or key == '\n':
                sys.stdout.write("\033[F")  
                sys.stdout.write("\033[K")  
                if current_row == 0: select_compression()           
                if current_row == 1: model_compression()           
                if current_row == 2: brute_force_compression()           
                if current_row == 3: benchmark()           
                if current_row == 4: create_config()           
            elif key.lower() == 'q':
                break

            sys.stdout.write("\033[{}A".format(7))
            print_menu(current_row)
    else:
        if args.command == "select_compression":
            select_compression_param(args.algorithm_name, args.input_filename, args.output_filename)
        elif args.command == "model_compression":
            model_compression_param(args.mode, args.input_filename, args.output_filename)
        elif args.command == "brute_force_compression":
            brute_force_param(args.input_filename, args.output_filename, args.delete_except_minimum)
        elif args.command == "benchmark":
            benchmark_param(args.selected_config_names, args.benchmark_type, args.output_to_file, args.output_plots)
        elif args.command == "create_config":
            create_config_param(args.name, args.executable_path, args.input_file_param, args.output_file_param, args.compression_params, args.decompression_params, args.extension)


if __name__ == "__main__":
    main()
