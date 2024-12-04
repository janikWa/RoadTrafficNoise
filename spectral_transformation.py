import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Funktion für STFT und Mel-Spektrogramm
def calculate_spectrograms(audio_path, output_dir):
    # Lade das Audiofile mit Librosa
    y, sr = librosa.load(audio_path, sr=22050)  # sr=22050 ist das Downsampling
    
    # Berechnung der STFT
    stft = librosa.stft(y, n_fft=2048, hop_length=1024, window='hann')  # Hanning-Fenster, Overlap 50%
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)  # dB-Skalierung
    
    # Berechnung des Mel-Spektrogramms
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=1024, n_mels=128)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)  # dB-Skalierung
    
    # Plot der Ergebnisse
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # STFT darstellen
    img1 = librosa.display.specshow(stft_db, sr=sr, hop_length=1024, x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set_title('STFT (dB)')
    fig.colorbar(img1, ax=ax[0], format='%+2.0f dB')

    # Mel-Spektrogramm darstellen
    img2 = librosa.display.specshow(mel_spectrogram_db, sr=sr, hop_length=1024, x_axis='time', y_axis='mel', ax=ax[1])
    ax[1].set_title('Mel-Spectrogram (dB)')
    fig.colorbar(img2, ax=ax[1], format='%+2.0f dB')

    plt.tight_layout()
    
    # Speichern des Plots
    filename = os.path.basename(audio_path).replace('.wav', '_spectrogram.png')
    plot_path = os.path.join(output_dir, filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Spektrogramme gespeichert: {plot_path}")

# Verzeichnis mit den vorverarbeiteten Audiodateien
preprocessed_dir = "/Users/Anton/Documents/KIT/Seminare/RTN/Audio rtn-samples/IDMT_Traffic/audio/Preprocessed_Audiofiles_Test"
output_dir = "/Users/Anton/Documents/KIT/Seminare/RTN/Audio rtn-samples/IDMT_Traffic/STFT_MELSPEC_Images"
os.makedirs(output_dir, exist_ok=True)

# Iteriere durch alle Audiodateien und berechne Spektrogramme
for file in os.listdir(preprocessed_dir):
    if file.endswith(".wav"):
        audio_path = os.path.join(preprocessed_dir, file)
        calculate_spectrograms(audio_path, output_dir)
