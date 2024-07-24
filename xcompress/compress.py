import subprocess
import timeit

def compress_with_config(config_data, input_file, output_file=""):
    """
    Compresses a file using specified compression configuration.

    Args:
        config_data (dict): Dictionary containing compression parameters, executable path, and file parameter placeholders.
        input_file (str): Path to the input file to be compressed.
        output_file (str, optional): Path to the output file. If not provided, defaults to generating a file based on config.

    Returns:
        tuple: A tuple containing the output file path and the compression execution time in nanoseconds.
    """
    try:
        compression_params = config_data["compression_params"]

        input_file_param = config_data["input_file_param"]
        input_file_param = input_file_param.replace("{input_file}", input_file)
        compression_params = [input_file_param if x == "@input_file_param" else x for x in compression_params]

        output_file_param = config_data["output_file_param"]
        if not output_file:
            if output_file_param != "stdout":
                output_file = output_file_param.replace("{output_file}", f"{input_file}.{config_data['extension']}")
            else:
                output_file = f"{input_file}.{config_data['extension']}"
        else:
            output_file_param = output_file_param.replace("{output_file}", output_file)
            compression_params = [x.replace("@output_file_param", output_file) if "@output_file_param" in x else x for x in compression_params]

        # Construct the command for compression
        command = [config_data["executable_path"]]
        command.extend(compression_params)

        # Start the timer
        start_time = timeit.default_timer()

        # Execute the compression command
        if output_file_param == "stdout":
            with open(output_file, "wb") as outfile:
                process = subprocess.Popen(command, stdout=outfile, stderr=subprocess.PIPE)
                process.communicate()
        else:
            process = subprocess.Popen(command, stderr=subprocess.PIPE)
            process.wait()

        # End the timer
        end_time = timeit.default_timer()
        execution_time_ns = (end_time - start_time) * 1e9

    except Exception as e:
        print(f"Error during compression: {e}")
        return "", 0

    return output_file, execution_time_ns