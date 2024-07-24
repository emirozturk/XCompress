# XCompress: LLM Assisted Python-based Text Compression Toolkit

XCompress is an adaptable tool designed to streamline the selection and evaluation of text compression algorithms. Leveraging a combination of manual selection, AI-driven recommendations (via CSM), brute-force optimization, and comprehensive benchmarking, XCompress empowers users to achieve optimal text compression for their specific requirements.

## Key Features

* **Manual Algorithm Selection:** Researchers and practitioners can exercise fine-grained control by manually choosing from a diverse set of established compression algorithms.
* **CSM-Guided Algorithm Recommendation:** The integrated CSM (Compression Selection Model) leverages artificial intelligence to intelligently suggest the most suitable algorithm based on user-defined priorities, such as minimizing compression time, decompression time, or achieving the highest compression ratio.
* **Brute-Force Optimization:** For scenarios demanding the absolute best compression, XCompress offers a brute-force search functionality that systematically evaluates all available algorithms to identify the one yielding the smallest compressed file size.
* **Comprehensive Benchmarking:** A robust benchmarking module facilitates direct comparison of algorithm performance on specified datasets, aiding in evidence-based decision-making.
* **Extensibility for Custom Algorithms:** XCompress allows users to seamlessly integrate and evaluate their own novel compression algorithms, fostering innovation and customization.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/emirozturk/XCompress.git
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**Interactive Mode**

Initiate the interactive mode by executing the following command:

```bash
python main.py
```

Navigate through the menu-driven interface using arrow keys and select options using the Enter key.

**Command-Line Interface (CLI)**

For scripted or automated workflows, utilize the command-line interface:

```bash
python main.py <command> [options]
```

**Command Reference**

*   `manual <algorithm_name> <input_filename> [--output_filename]`
    *   `algorithm_name`: The identifier of the desired compression algorithm (e.g., "gzip", "bzip2", "lzma").
    *   `input_filename`: The path to the text file to be compressed.
    *   `--output_filename` (optional): The name to be assigned to the resulting compressed file.

*   `csm <mode> <input_filename> [--output_filename]`
    *   `mode`: Specify the optimization goal: "fast-compression", "fast-decompression", or "best-compression".
    *   `input_filename`: The path to the text file.
    *   `--output_filename` (optional): The name for the compressed file.

*   `brute_force <input_filename> <delete_except_minimum>`
    *   `input_filename`: The path to the text file.
    *   `delete_except_minimum`: Set to "True" to retain only the smallest compressed file generated during the brute-force process.

*   `benchmark <benchmark_type> <input_filename> <output_to_file> <output_plots> <algorithm_names> [--output_filename]`
    *   `benchmark_type`: Choose "compress" for compression-only benchmarks or "compress_decompress" for compression and decompression benchmarks.
    *   `input_filename`: The path to the text file.
    *   `output_to_file`: Set to "True" to save benchmark results in a structured file format.
    *   `output_plots`: Set to "True" to generate visual plots summarizing the benchmark results.
    *   `algorithm_names`: A space-separated list of algorithm names or custom configuration names to include in the benchmark.

*   `config_creation <name> <executable_path> <input_file_param> <output_file_param> <compression_params> <decompression_params> <extension>`
    *   Detailed parameters for defining custom compression algorithm configurations (refer to code documentation for guidance).

## Contributing

Contributions that enhance the functionality, usability, or documentation of XCompress are warmly welcomed. Please adhere to established code style guidelines and provide comprehensive documentation for any new features or modifications.


## License

This project is licensed under the MIT License.
