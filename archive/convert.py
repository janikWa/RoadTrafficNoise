import pandas as pd 
import numpy as np
import os 
from scipy.io import wavfile

# function for decibel compression 
def convert(file_path): 
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) == 2:
        data = np.mean(data, axis=1)  

    if data.dtype == np.int16:  # 16-Bit Integer
        max_amplitude = 32768.0
    elif data.dtype == np.int32:  # 32-Bit Integer
        max_amplitude = 2147483648.0
    elif data.dtype == np.float32:  # 32-Bit Float
        max_amplitude = 1.0
    else:
        max_amplitude = np.max(np.abs(data))  

    # dB calculation
    data = np.where(data == 0, np.finfo(float).eps, data) 
    dbfs_data = 20 * np.log10(np.abs(data) / max_amplitude)

    reference_spl = 94  
    spl_data = dbfs_data + reference_spl

    average_spl = np.mean(spl_data)
    return average_spl


path = "df_dataset.xlsx"
df = pd.read_excel(path)

df["Dezibel_ber"] = np.nan

directory = "/Users/janikwahrheit/Library/CloudStorage/OneDrive-Persönlich/01_Studium/01_Bachelor/05. WS_2024_25/Seminar RTN/audio"  

for file in os.listdir(directory):
    filename = os.fsdecode(file)  
    print(filename)
    if filename.endswith(".wav"): 
        file_path = os.path.join(directory, filename)  
        try:
            decibel = convert(file_path)  
            filename_without_extension = filename.replace(".wav", "")  
            df.loc[df['file'] == filename_without_extension, "Dezibel_ber"] = decibel
        except FileNotFoundError:
            print(f"Datei nicht gefunden: {file_path}")
        
df.to_excel("Uncleaned.xlsx")
