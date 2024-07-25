import argparse
import readchar
import sys
from .select_compression import select_compression, select_compression_param
from .csm import model_compression, model_compression_param
from .benchmark import benchmark, benchmark_param
from .brute_force import brute_force_compression, brute_force_param
from .create_config import create_config, create_config_param
from .util import clear_screen
from .visualization import visualization, visualization_param


class CustomHelpAction(argparse.Action):
    """
    A custom argparse action that displays help information for both the main parser and its subparsers.

    This action overrides the default help behavior to include detailed help messages for all available subcommands.

    Methods:
        __init__: Initializes the CustomHelpAction instance.
        __call__: Displays help information for the parser and its subparsers.
    """

    def __init__(
        self,
        option_strings,
        dest=argparse.SUPPRESS,
        default=argparse.SUPPRESS,
        help=None,
    ):
        """
        Initializes the CustomHelpAction.

        Args:
            option_strings (list): The option strings for this action.
            dest (str): The destination for the parsed value (default: argparse.SUPPRESS).
            default (any): The default value (default: argparse.SUPPRESS).
            help (str): The help message (default: None).
        """
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Displays help information for the parser and its subparsers.

        Args:
            parser (argparse.ArgumentParser): The parser to display help for.
            namespace (argparse.Namespace): The namespace for the parsed values.
            values (any): The values for the action (default: None).
            option_string (str): The option string (default: None).
        """
        parser.print_help()
        subparsers_actions = [
            action
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print(f"{choice}:")
                print(subparser.format_help())
        parser.exit()


menu = [
    "Select compression algorithm",
    "Use CSM (LLM) for auto algorithm selection",
    "Find best compression using brute force",
    "Get benchmark results for specific file",
    "Create config for custom compression algorithm",
    "Visualize benchmark results",
]


def print_menu(selected_row):
    """
    Prints the main menu for the XCompress tool.

    Args:
        selected_row (int): The index of the currently selected menu item to highlight.
    """
    clear_screen()
    print(
        "\n\033[1mXCompress\033[0m is a tool for selecting the best text compression algorithm for a given input."
    )
    print(
        "You can choose any algorithm you want, determine the best compression or fastest compression algorithm with CSM,"
    )
    print("and select the best compression algorithm with brute force.\n")
    print("Please make a selection:\n")
    for idx, row in enumerate(menu):
        if idx == selected_row:
            print("\033[1;32m->\033[0m", "\033[1;32m", row, "\033[0m")
        else:
            print("   ", row)
    print("Press q to quit")


def main():
    """
    The main entry point for the XCompress tool.

    This function sets up the command-line argument parser and handles user input through either command-line arguments or an interactive menu.
    - For command-line arguments, it parses the arguments and calls the appropriate function based on the specified command.
    - For interactive mode, it displays a menu for the user to select various functionalities such as selecting a compression algorithm, benchmarking, creating configurations, and visualizing results.
    """
    parser = argparse.ArgumentParser(
        description="XCompress Compression Tool", add_help=False
    )
    parser.add_argument(
        "-h", "--help", action=CustomHelpAction, help="show this help message and exit"
    )

    subparsers = parser.add_subparsers(dest="command", required=False)

    # Select Compression (with help message)
    parser_select_compression = subparsers.add_parser(
        "manual", help="Selects a specific compression algorithm for the input file."
    )
    parser_select_compression.add_argument(
        "algorithm_name", help="The name of the compression algorithm to use."
    )
    parser_select_compression.add_argument(
        "input_filename", help="The path to the file to compress."
    )
    parser_select_compression.add_argument(
        "--output_filename",
        default=None,
        help="The path to save the compressed file (defaults to input filename with .<algorithm> extension).",
    )

    # Model Compression (with help message)
    parser_model_compression = subparsers.add_parser(
        "csm",
        help="Uses CSM (LLM) to automatically select the best compression algorithm based on your preferences (Fast compression, Fast decompression or Best compression).",
    )
    parser_model_compression.add_argument(
        "mode",
        choices=["fast-compression", "fast-decompression", "best-compression"],
        help="The optimization mode for CSM (fast compression, fast decompression or best compression).",
    )
    parser_model_compression.add_argument(
        "input_filename", help="The path to the file to compress."
    )
    parser_model_compression.add_argument(
        "--output_filename",
        default=None,
        help="The path to save the compressed file (defaults to input filename with .<algorithm> extension).",
    )

    # Brute Force Compression (with help message)
    parser_brute_force = subparsers.add_parser(
        "brute_force",
        help="Finds the best compression algorithm for the input file by trying all available algorithms and keeping the one with the smallest size.",
    )
    parser_brute_force.add_argument(
        "input_filename", help="The path to the file to compress."
    )
    parser_brute_force.add_argument(
        "out_folder", help="Directory where output files are stored."
    )
    parser_brute_force.add_argument(
        "--delete_except_minimum",
        action="store_true",
        help="Whether to delete all compressed files except the one with the smallest size (default: False).",
    )

    # Benchmark (with help message)
    parser_benchmark = subparsers.add_parser(
        "benchmark",
        help="Runs benchmarks on specified compression configurations and outputs results to file or plots.",
    )
    parser_benchmark.add_argument(
        "benchmark_type",
        choices=["compress", "compress_decompress"],
        help="The type of benchmark to run (compression or compression-decompression).",
    )
    parser_benchmark.add_argument(
        "input_filename", help="The path to the file to compress."
    )
    parser_benchmark.add_argument(
        "--output_to_file",
        action="store_true",
        help="Whether to output results to a file",
    )
    parser_benchmark.add_argument(
        "--output_plots",
        action="store_true",
        help="Whether to generate plots from the benchmark results.",
    )
    parser_benchmark.add_argument(
        "algorithm_names",
        nargs="+",
        help="Space-separated list of config names to benchmark.",
    )
    parser_benchmark.add_argument(
        "--output_filename",
        default=None,
        help="The path to save the compressed file (defaults to input filename with .<algorithm> extension).",
    )

    # Create Config (with help message)
    parser_create_config = subparsers.add_parser(
        "config_creation",
        help="Creates a configuration file for a custom compression algorithm.",
    )
    parser_create_config.add_argument("name", help="The name of the new configuration.")
    parser_create_config.add_argument(
        "executable_path",
        help="The path to the executable for the compression algorithm.",
    )
    parser_create_config.add_argument(
        "--input_file_param",
        default=None,
        help="The parameter for the input file in the executable command (optional).",
    )
    parser_create_config.add_argument(
        "--output_file_param",
        default=None,
        help="The parameter for the output file in the executable command (optional).",
    )
    parser_create_config.add_argument(
        "--compression_params",
        nargs="*",
        help="List of parameters for the compression process.",
    )
    parser_create_config.add_argument(
        "--decompression_params",
        nargs="*",
        help="List of parameters for the decompression process (if applicable).",
    )
    parser_create_config.add_argument(
        "extension",
        help="The file extension to use for compressed files generated by this configuration.",
    )

    # Visualization (with help message)
    parser_visualization = subparsers.add_parser(
        "visualization", help="Visualizes benchmark results from specified JSON files."
    )
    parser_visualization.add_argument(
        "file_path", help="The path to the JSON file to visualize."
    )

    args = parser.parse_args()

    if args.command is None:
        current_row = 0
        print_menu(current_row)
        while True:
            key = readchar.readkey()
            if key == readchar.key.UP and current_row > 0:
                current_row -= 1
            elif key == readchar.key.DOWN and current_row < 5:
                current_row += 1
            elif key == "\r" or key == "\n":
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                if current_row == 0:
                    select_compression()
                elif current_row == 1:
                    model_compression()
                elif current_row == 2:
                    brute_force_compression()
                elif current_row == 3:
                    benchmark()
                elif current_row == 4:
                    create_config()
                elif current_row == 5:
                    visualization()
            elif key.lower() == "q":
                break

            sys.stdout.write("\033[{}A".format(8))
            print_menu(current_row)
    else:
        if args.command == "manual":
            select_compression_param(
                args.algorithm_name, args.input_filename, args.output_filename
            )
        elif args.command == "csm":
            model_compression_param(
                args.mode, args.input_filename, args.output_filename
            )
        elif args.command == "brute_force":
            brute_force_param(
                args.input_filename, args.out_folder, args.delete_except_minimum
            )
        elif args.command == "benchmark":
            benchmark_param(
                args.algorithm_names,
                args.benchmark_type,
                args.input_filename,
                args.output_filename,
                args.output_to_file,
                args.output_plots,
            )
        elif args.command == "config_creation":
            create_config_param(
                args.name,
                args.executable_path,
                args.input_file_param,
                args.output_file_param,
                args.compression_params,
                args.decompression_params,
                args.extension,
            )
        elif args.command == "visualization":
            visualization_param(args.file_path)
        elif args.command == "help":
            for subparser in [
                parser_select_compression,
                parser_model_compression,
                parser_brute_force,
                parser_benchmark,
                parser_create_config,
                parser_visualization,
            ]:
                print("\n" + subparser.prog)
                subparser.print_help()


if __name__ == "__main__":
    main()
