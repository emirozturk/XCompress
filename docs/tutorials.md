# XCompress Command Line Tool Examples

The `XCompress` tool provides functionalities for text compression, benchmarking, configuration creation, and visualization. Below is a guide on how to use each command available in the tool.

## 1. Select Compression Algorithm

**Command:** `manual`

**Description:** Selects a specific compression algorithm to use for compressing a given file.

**Usage:**
```bash
python main.py manual <algorithm_name> <input_filename> [--output_filename <output_filename>]
```

**Arguments:**
- `algorithm_name` (str): The name of the compression algorithm to use.
- `input_filename` (str): The path to the file to compress.
- `--output_filename` (optional, str): The path to save the compressed file. If not provided, the output file will have the same name as the input file with an extension corresponding to the algorithm.

**Example:**
```bash
python main.py manual gzip input.txt --output_filename input_compressed.gz
```

For example, for compressing nattest.txt with gzip, input below could be given and as a result, filename and compression time in nanoseconds will be printed:

```bash
(base) xcompress % python main.py manual gzip nattest.txt
Compression completed successfully. Filename is ('nattest.txt.gz', 9587125.154212117)
```
---

## 2. Use CSM for Auto Algorithm Selection

**Command:** `csm`

**Description:** Uses the CSM (LLM) model to automatically select the best compression algorithm based on the specified mode.

**Usage:**
```bash
python main.py csm <mode> <input_filename> [--output_filename <output_filename>]
```

**Arguments:**
- `mode` (str): The optimization mode for CSM. Choices are `fast-compression`, `fast-decompression`, and `best-compression`.
- `input_filename` (str): The path to the file to compress.
- `--output_filename` (optional, str): The path to save the compressed file. If not provided, the output file will have the same name as the input file with an extension corresponding to the selected algorithm.

**Example:**
```bash
python main.py csm fast-compression input.txt --output_filename input_csm.gz
```

As an example, if best-compression is desired, the command can be used as:

```bash
(base) xcompress % python main.py csm best-compression nattest.txt
```

And the output will be generated as:

```bash
Selected compression algorithm: gzip
Input filename: nattest.txt
Output filename: None
Compression completed successfully. Filename is nattest.txt.gz
Press any key to return to menu
```

---

## 3. Find Best Compression Using Brute Force

**Command:** `brute_force`

**Description:** Finds the best compression algorithm by trying all available algorithms and selecting the one with the smallest file size.

**Usage:**
```bash
python main.py brute_force <input_filename> <out_folder> <delete_except_minimum>
```

**Arguments:**
- `input_filename` (str): The path to the file to compress.
- `out_folder` (str): The path compressed files are stored.
- `delete_except_minimum` (bool): Whether to delete all compressed files except the one with the smallest size.

**Example:**
```bash
python main.py brute_force input.txt ./output True
```

As an example, to compress a file with brute_force commmand below can be used:

```bash
(base) xcompress % python main.py brute_force nattest.txt ./output True
```

Then brue_force module will output the process like:

```bash
Trying brotli...
Trying gzip...
Trying NNCP...
Trying bzip2...
Trying ngram-compressor...
Trying LZW...
Trying Snappy-Snzip...
Trying LZMA...
Trying zpaq...
Trying zstd...
Trying zlib...
Trying PPM...
Trying lz4...
```

Here, it will try the algorithms defined in compression_configs directory. After finishing, the module will find the algorithm with the best compression ratio and output:

```bash
Selected compression algorithm: gzip
Input filename: nattest.txt
Output filename: output/nattest.txt.gzip
Compression completed successfully. Filename is nattest.txt.gz
```

---

## 4. Get Benchmark Results for a Specific File

**Command:** `benchmark`

**Description:** Runs benchmarks on specified compression configurations and outputs the results to a file or generates plots.

**Usage:**
```bash
python main.py benchmark <benchmark_type> <input_filename> <output_to_file> <output_plots> <algorithm_names> [--output_filename <output_filename>]
```

**Arguments:**
- `benchmark_type` (str): The type of benchmark to run. Choices are `compress` or `compress_decompress`.
- `input_filename` (str): The path to the file to compress.
- `output_to_file` (bool): Whether to output results to a file.
- `output_plots` (bool): Whether to generate plots from the benchmark results.
- `algorithm_names` (list of str): Space-separated list of configuration names to benchmark.
- `--output_filename` (optional, str): The path to save the benchmark results file.

**Example:**
```bash
python main.py benchmark compress input.txt True True gzip bzip2 --output_filename benchmark_results.json
```

For example, to compress the nattest file using lz4 and gzip and then save the compression and decompression speed results and ratio results for future use and plotting, you can use the following command:

```bash
python main.py benchmark compress-decompress nattest.txt gzip lz4 --output_plots --output_to_file
```

The application will produce output like the following for the selected methods:

```bash
Selected compression algorithm: gzip
Input filename: /Users/emirozturk/Desktop/nattest.txt
Output filename: nattest.txt.gz
Selected compression algorithm: lz4
Input filename: /Users/emirozturk/Desktop/nattest.txt
Output filename: nattest.txt.lz4
```

The plot module will then run in the application, and the following screenshot will be displayed.
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/visualization.png?raw=true)


---

## 5. Create Config for Custom Compression Algorithm

**Command:** `config_creation`

**Description:** Creates a configuration file for a custom compression algorithm.

**Usage:**
```bash
python main.py config_creation <name> <executable_path> --input_file_param <input_file_param> --output_file_param <output_file_param> <compression_params> <decompression_params> <extension>
```

**Arguments:**
- `name` (str): The name of the new configuration.
- `executable_path` (str): The path to the executable for the compression algorithm.
- `input_file_param` (str): The parameter for the input file in the executable command.
- `output_file_param` (str): The parameter for the output file in the executable command.
- `compression_params` (str): Space-separated list of parameters for the compression process.
- `decompression_params` (str): Space-separated list of parameters for the decompression process (if applicable).
- `extension` (str): The file extension to use for compressed files generated by this configuration.

**Example:**
```bash
python main.py config_creation custom_config /path/to/compressor --input_file_param -i --output_file_param -o --compression_params -p1 --decompression_params -p2 .custom
```

To generate a configuration, it is necessary to know the flags of the compression method to be used. For example, for the gzip method, the compression can be given on the console as `gzip -c inputfilename`. However, if additional tasks are required, they can also be added. For example, to overwrite the compressed file even if it already exists, `-f` can be added. Similarly, during decompression, the gzip executable should be run with `-d inputfile`. The following parameters can be used to generate such a configuration:

```bash
python main.py config_creation gzip_with_force gzip --compression_params -c -k --decompression_params -d -k gz
```

Here, the input file or output file parameters are left empty because they are not needed.

For example, the `snzip` implementation outputs the compressed result to the console by default. To redirect this to a file, the `stdout` parameter should be used.

```bash
python main.py config_creation snzip_with_console --compression_params -k -c --decompression_params -d -k -c --output_file_param stdout sz
```

With the provided `stdout`, XCompress will read the data from the standard output.

---

## 6. Visualize Benchmark Results

**Command:** `visualization`

**Description:** Visualizes benchmark results from specified JSON file.

**Usage:**
```bash
python main.py visualization <file_path>
```

**Arguments:**
- `file_path` (list of str): Path to JSON file containing metrics like compressed size, compression time, and optionally decompression time.

**Example:**
```bash
python main.py visualization results1.json
```

For example, to read the file obtained from the benchmark above, you can use the following command:

```bash
python main.py visualization benchmark_results.json
```

As a result, the visualization module will run in the browser and generate the plots.  
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/plot5.png?raw=true)

You can select and plot three different results separately if desired.  
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/plot1.png?raw=true)  
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/plot3.png?raw=true)  
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/plot4.png?raw=true)

Additionally, real-time methods or results can be extracted and added to the plot.  
![alt text](https://github.com/emirozturk/xcompress/blob/main/docs/Images/plot2.png?raw=true)

Moreover, the library provides support for resizing, autoscaling, and other features. The generated plots can also be downloaded.