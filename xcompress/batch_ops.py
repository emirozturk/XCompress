import os
import json
from compress import compress_with_config
from decompress import decompress_with_config

def get_configs():
    """
    Retrieves compression configuration data from JSON files located in the `compression_configs` directory.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the configuration data loaded from a JSON file.
    """
    directory = os.path.join(os.path.dirname(__file__), "compression_configs")
    files = os.listdir(directory)
    config_data = []
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(directory, file)
            with open(file_path, "r") as f:
                config_data.append(json.load(f))
    return config_data


def batch_compress_decompress(input_file, out_folder, skip_if_file_exists):
    """
    Compresses and decompresses a file using multiple compression configurations, returns performance metrics for each configuration.
    Not reachable from cli or menu. For getting batch results for all defined config files. These results are used to train CSM module.

    Args:
        input_file (str): The path to the input file to be compressed and decompressed.
        out_folder (str): The directory where output files will be saved.
        skip_if_file_exists (bool): If True, skips compression if the output file already exists.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing metrics for each compression configuration,
                              including file sizes and times for compression and decompression.
    """
    configs = get_configs()
    result_list = []
    for config_file in configs:
        name = config_file["name"]
        extension = config_file["extension"]

        if not os.path.exists(os.path.join(out_folder, name)):
            os.makedirs(os.path.join(out_folder, name))
        out_file_name = os.path.join(out_folder, name, f"{os.path.basename(input_file)}.{extension}")
        if skip_if_file_exists and os.path.exists(out_file_name):
            print(f"Skipping... File exists for method: {name} for file: {input_file}")
            continue
        output_file, compression_time_ns = compress_with_config(config_file, input_file, out_file_name)
        if output_file != "":
            _, decompression_time_ns = decompress_with_config(config_file, output_file)

            file_size = os.path.getsize(input_file)
            compressed_size = os.path.getsize(output_file)
            result_list.append({
                "filename": input_file,
                "name": name,
                "file_size": file_size,
                "compressed_size": compressed_size,
                "compression_time_ns": compression_time_ns,
                "decompression_time_ns": decompression_time_ns
            })
    return result_list


def batch_compress(input_file):
    """
    Compresses a file using multiple compression configurations and returns performance metrics.

    Args:
        input_file (str): The path to the input file to be compressed.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing metrics for each compression configuration,
                              including file sizes and compression times.
    """
    config_files = get_configs()
    result_list = []
    for config_file in config_files:
        name = config_file["name"]
        output_file, compression_time_ns = compress_with_config(config_file, input_file)
        file_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        result_list.append({
            "name": name,
            "file_size": file_size,
            "compressed_size": compressed_size,
            "compression_time_ns": compression_time_ns
        })
    return result_list
