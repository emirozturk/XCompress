import os
import json
from batch_ops import batch_compress_decompress 

directories = ["/mnt/c/USers/emiro/Desktop/ProjectX/Dataset/NatLang",
               "/mnt/c/USers/emiro/Desktop/ProjectX/Dataset/ProgLang",
               "/mnt/c/USers/emiro/Desktop/ProjectX/Dataset/Sensordata",
               "/mnt/c/USers/emiro/Desktop/ProjectX/Dataset/Sql"
               ]

for directory in directories:
    files = os.listdir(directory)
    text_files = [file for file in files if file.endswith(".txt")]
    results = []
    results_file_path = f"{directory}_results.json"
    
    if os.path.exists(results_file_path):
        with open(results_file_path, "r") as json_file:
            previous_results = json.load(json_file)
            results.extend(previous_results)

    for text_file in text_files:
        try:
            result = batch_compress_decompress(os.path.join(directory,text_file),"/mnt/c/USers/emiro/Desktop/ProjectX/CompressedFiles",skip_if_file_exists=True)
            results.extend(result)
            with open(results_file_path, "w") as json_file:
                json.dump(results, json_file)
        except:
            pass