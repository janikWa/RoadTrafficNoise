import os
import numpy as np
from scipy.io import wavfile
from scipy import signal

# Funktion für Audio-Preprocessing
def preprocess_audio(file_path, output_directory, target_sample_rate=22000):
    sample_rate, data = wavfile.read(file_path)

    # Mono-Konvertierung
    if len(data.shape) == 2:
        data = np.mean(data, axis=1)

    # Downsampling
    if sample_rate != target_sample_rate:
        num_samples = int(len(data) * target_sample_rate / sample_rate)
        data = signal.resample(data, num_samples)

    # Normalisierung
    data_mean = np.mean(data)
    data_std = np.std(data)
    if data_std > 0:
        data = (data - data_mean) / data_std

    # Speichern der vorverarbeiteten Datei
    preprocessed_filename = os.path.basename(file_path).replace(".wav", "_preprocessed.wav")
    output_path = os.path.join(output_directory, preprocessed_filename)
    wavfile.write(output_path, target_sample_rate, data.astype(np.float32))

    print(f"Vorverarbeitete Datei gespeichert: {output_path}")

# Pfade einstellen
input_directory = "/Users/Anton/Documents/KIT/Seminare/RTN/Audio rtn-samples/IDMT_Traffic/audio"  # Hier den Pfad zu den Originaldateien einfügen
output_directory = "/Users/Anton/Documents/KIT/Seminare/RTN/Audio rtn-samples/IDMT_Traffic/audio/Preprocessed_Audiofiles"  # Hier den Pfad für die Ausgabe einfügen
os.makedirs(output_directory, exist_ok=True)  # Ordner erstellen, falls nicht vorhanden

# Schleife zum Verarbeiten der .wav-Dateien
for file in os.listdir(input_directory):
    filename = os.fsdecode(file)
    if filename.endswith(".wav"):
        file_path = os.path.join(input_directory, filename)
        preprocess_audio(file_path, output_directory)

        
