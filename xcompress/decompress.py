import json
import subprocess
import timeit
import os

def decompress_with_config(config_data,input_file,output_file=""):
    """
    Decompresses a file using the specified configuration parameters.

    Args:
        config_data (dict): A dictionary containing configuration details such as 
                            executable path, decompression parameters, and file parameters.
        input_file (str): Path to the file that needs to be decompressed.
        output_file (str): Path to the file where the decompressed output should be saved.
                           If not specified, a default name based on the input file is used.

    Returns:
        tuple: A tuple containing:
            - output_file (str): Path to the decompressed file.
            - execution_time_ns (float): Time taken for decompression in nanoseconds.
    """
    try:
        decompression_params = config_data["decompression_params"]

        input_file_param = config_data["input_file_param"]
        input_file_param = input_file_param.replace("{input_file}",input_file)
        decompression_params = [input_file_param if x == "@input_file_param" else x for x in decompression_params]

        
        output_file_param = config_data["output_file_param"]
        if output_file=="":
            base_filename, _ = os.path.splitext(input_file)
            file_name_without_extension,extension = os.path.splitext(base_filename)        
            output_file = f"{file_name_without_extension}.o{extension}"        
            if output_file_param != "stdout":
                decompression_params = [x.replace("@output_file_param",output_file) if "@output_file_param" in x else x for x in decompression_params]

        else:            
            output_file_param.replace("{output_file}",output_file)
            decompression_params = [x.replace("@output_file_param",output_file) if "@output_file_param" in x else x for x in decompression_params]
    
        command = [config_data["executable_path"]]
        command.extend(decompression_params)

        start_time = timeit.default_timer()
        
        if output_file_param == "stdout":
            with open(output_file, "wb") as outfile:
                process = subprocess.Popen(command, stdout=outfile,stderr=subprocess.PIPE)
        else:        
            process = subprocess.Popen(command,stderr=subprocess.PIPE)
        process.wait()

        end_time = timeit.default_timer()
        execution_time_ns = (end_time - start_time) * 1e9
    except Exception as e:
        return e
    
    return output_file,execution_time_ns