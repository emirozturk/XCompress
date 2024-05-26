## XCompress: Intelligent Text Compression

XCompress is your go-to tool for finding the most efficient text compression algorithm. It empowers you with manual selection, AI-powered recommendations, brute-force optimization, and performance benchmarking.

### Features

* **Manual Selection:** Choose from a variety of compression algorithms based on your specific needs.
* **AI-Powered Selection (BCM):** Let our intelligent model (BCM) recommend the best algorithm for fast compression, fast decompression, or the best overall compression ratio.
* **Brute Force Optimization:** Systematically test all available algorithms to discover the absolute best compression for your file.
* **Benchmarking:** Compare the performance of different algorithms on your chosen file.
* **Custom Configurations:** Easily integrate and use your own compression algorithms.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/emirozturk/XCompress.git
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

**Interactive Menu**

Launch the interactive menu by simply running the script:

```bash
python main.py
```

Navigate using arrow keys and press Enter to select options.

**Command Line Interface (CLI)**

For more precise control, use the following command structure:

```bash
python main.py <command> [options]
```

**Command Details**

*   `manual <algorithm_name> <input_filename> [--output_filename]`
    *   `algorithm_name`: The name of the compression algorithm (e.g., "gzip", "bzip2", "lzma").
    *   `input_filename`: The path to the text file you want to compress.
    *   `--output_filename` (optional): The desired name for the compressed file.

*   `bcm <mode> <input_filename> [--output_filename]`
    *   `mode`: Choose between "fast-compression", "fast-decompression", or "best-compression".
    *   `input_filename`: The path to the text file.
    *   `--output_filename` (optional): The name for the compressed file.

*   `brute_force <input_filename> <delete_except_minimum>`
    *   `input_filename`: The path to the text file.
    *   `delete_except_minimum`: Set to "True" to keep only the smallest compressed file.

*   `benchmark <benchmark_type> <input_filename> <output_to_file> <output_plots> <algorithm_names> [--output_filename]`
    *   `benchmark_type`: Either "compress" (compression only) or "compress_decompress" (compression and decompression).
    *   `input_filename`: The path to the text file.
    *   `output_to_file`: Set to "True" to save results to a file.
    *   `output_plots`: Set to "True" to generate plots.
    *   `algorithm_names`: A space-separated list of algorithm names or configuration names to benchmark (e.g., "gzip lzma my_custom_config").

*   `config_creation <name> <executable_path> <input_file_param> <output_file_param> <compression_params> <decompression_params> <extension>`
    *   Detailed parameters for creating custom configurations (refer to code comments or documentation for guidance).

### Examples

**Manual Compression (Bzip2):**

```bash
python main.py manual bzip2 my_document.txt --output_filename my_document_compressed.bz2
```

**AI Selection (Fast Decompression):**

```bash
python main.py bcm fast-decompression my_log_file.txt
```
**Brute Force Compression:**
```bash
python main.py brute_force my_log_file.txt
```
**Benchmark:**
```bash
python main.py benchmark compress my_text_file.txt True True gzip bzip2 lzma
```

### Contributing

Contributions are highly appreciated! Feel free to open issues to report problems or submit pull requests with enhancements.

### License

This project is licensed under the MIT License.
