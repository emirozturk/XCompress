"""
XCompress: LLM Assisted Python-based Text Compression Toolkit

XCompress is an adaptable tool designed to streamline the selection and evaluation of text compression algorithms. Leveraging a combination of manual selection, AI-driven recommendations (via CSM), brute-force optimization, and comprehensive benchmarking, XCompress empowers users to achieve optimal text compression for their specific requirements.
"""

"""
Module: select_compression

This module provides functionality for selecting a specific compression algorithm for an input file.

Functions:
- select_compression: Prompts the user to select a compression algorithm from a list.
- select_compression_param: Executes the compression process with the specified algorithm and parameters.

Usage example:
    python main.py manual gzip example.txt --output_filename example.txt.gz
"""

"""
Module: csm

This module utilizes the CSM (Compression Selection Model) to automatically select the best compression algorithm based on user preferences.

Functions:
- model_compression: Prompts the user to select an optimization mode for compression.
- model_compression_param: Executes the compression process with the specified optimization mode and parameters.

Usage example:
    python main.py csm best-compression example.txt --output_filename example.txt.gz
"""

"""
Module: benchmark

This module runs benchmarks on specified compression configurations and outputs the results.

Functions:
- benchmark: Prompts the user to select benchmark options interactively.
- benchmark_param: Executes the benchmark process with the specified parameters.

Usage example:
    python main.py benchmark compress example.txt True True gzip bzip2 --output_filename benchmark_results.json
"""

"""
Module: brute_force

This module finds the best compression algorithm for an input file by trying all available algorithms and selecting the one with the smallest size.

Functions:
- brute_force_compression: Prompts the user to perform brute-force compression.
- brute_force_param: Executes the brute-force compression process with the specified parameters.

Usage example:
    python main.py brute_force example.txt True
"""

"""
Module: create_config

This module creates configuration files for custom compression algorithms.

Functions:
- create_config: Prompts the user to create a configuration file for a custom compression algorithm.
- create_config_param: Executes the creation of the configuration file with specified parameters.

Usage example:
    python main.py config_creation myconfig /path/to/executable input_file output_file param1 param2 .ext
"""

"""
Module: visualization

This module visualizes benchmark results from specified JSON files.

Functions:
- visualization: Prompts the user to select visualization options interactively.
- visualization_param: Executes the visualization process with the specified parameters.

Usage example:
    python main.py visualization results1.json results2.json
"""
from .csm import model_compression, model_compression_param, print_menu
from .util import clear_screen, load_configs, get_config
from .compress import compress_with_config
from .llm_model import detect_algorithm

__all__ = [
    "model_compression",
    "model_compression_param",
    "print_menu",
    "clear_screen",
    "load_configs",
    "get_config",
    "compress_with_config",
    "detect_algorithm",
]