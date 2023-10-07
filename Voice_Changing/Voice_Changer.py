import wave
import os
import librosa
import soundfile as sf
import pyttsx3
from random import randint

# Text, der gesprochen werden soll
text = "Hallo, das ist ein Beispieltext, der gesprochen wird."

# Konfigurieren Sie pyttsx3
engine = pyttsx3.init()

# Sprechen Sie den Text
engine.save_to_file(text, "gesprochen.wav")
engine.runAndWait()

def pitch(segment_path, pitch_factor):
    # Öffnen Sie die WAV-Datei
    audio, sample_rate = librosa.load(segment_path, sr=None)

    # Verwenden Sie den Phase Vocoder, um die Tonhöhe zu ändern
    audio_pitch_shifted = librosa.effects.pitch_shift(audio, sr=sample_rate, n_steps=pitch_factor)

    # Speichern Sie das geänderte Audio als WAV-Datei
    sf.write(segment_path, audio_pitch_shifted, sample_rate)

# Pfad zur Eingabe-WAV-Datei
input_wav_path = "gesprochen.wav"
processing_folder = "Processing"

# Löschen Sie den Inhalt des "Processing"-Ordners, falls vorhanden
for item in os.listdir(processing_folder):
    item_path = os.path.join(processing_folder, item)
    if os.path.isfile(item_path):
        os.remove(item_path)

# Öffnen Sie die Eingabe-WAV-Datei
input_wav = wave.open(input_wav_path, "rb")

# Holen Sie die Abtastrate (Sample Rate) und die Anzahl der Frames
sample_rate = input_wav.getframerate()
num_frames = input_wav.getnframes()

# Definieren Sie die Länge jedes Sekundenabschnitts (in Sekunden)
segment_laenge_s = 1

# Erstellen Sie den Ordner "Processing", falls er nicht existiert
output_folder = "Processing"
os.makedirs(output_folder, exist_ok=True)

# Lesen Sie die WAV-Daten
wav_data = input_wav.readframes(num_frames)

# Schließen Sie die Eingabe-WAV-Datei
input_wav.close()

# Konvertieren Sie die WAV-Daten in ein NumPy-Array
import numpy as np
audio_array = np.frombuffer(wav_data, dtype=np.int16)

# Berechnen Sie die Anzahl der Frames pro Sekundenabschnitt
frames_per_segment = int(sample_rate * segment_laenge_s)

# Teilen Sie die WAV-Datei in Sekundenabschnitte auf und speichern Sie sie im Ordner "Processing"
for i, start_frame in enumerate(range(0, len(audio_array), frames_per_segment)):
    end_frame = start_frame + frames_per_segment
    segment_data = audio_array[start_frame:end_frame]
    
    # Erstellen Sie eine neue WAV-Datei für den Sekundenabschnitt
    output_wav_path = os.path.join(output_folder, f"segment_{i}.wav")
    output_wav = wave.open(output_wav_path, "wb")
    output_wav.setnchannels(input_wav.getnchannels())
    output_wav.setsampwidth(input_wav.getsampwidth())
    output_wav.setframerate(sample_rate)
    output_wav.writeframes(segment_data.tobytes())
    output_wav.close()
    
    # Ändern Sie die Tonhöhe des Segments
    pitch(output_wav_path, randint(-5, 10))  # Zufällige Tonhöhenänderung

print(f"{i+1} Sekundenabschnitte wurden im Ordner 'Processing' gespeichert und die Tonhöhe wurde geändert.")

# Jetzt können Sie die WAV-Dateien aus dem "Processing"-Ordner hintereinander fügen.
# Hier ist der Code, um die .wav-Dateien zu kombinieren:

import wave

# Pfad zum Ordner mit den geänderten und segmentierten .wav-Dateien
processing_folder = "Processing"

# Sammeln Sie alle .wav-Dateien im Ordner
wav_files = [file for file in os.listdir(processing_folder) if file.endswith(".wav")]

# Öffnen Sie die erste .wav-Datei, um die Abtastrate und den Samplewidth zu erhalten
first_wav_path = os.path.join(processing_folder, wav_files[0])
first_wav = wave.open(first_wav_path, "rb")
sample_rate = first_wav.getframerate()
sample_width = first_wav.getsampwidth()

# Erstellen Sie eine neue .wav-Datei zum Speichern des kombinierten Audios
combined_wav_path = "combined_audio.wav"
combined_wav = wave.open(combined_wav_path, "wb")
combined_wav.setnchannels(first_wav.getnchannels())
combined_wav.setsampwidth(sample_width)
combined_wav.setframerate(sample_rate)

# Fügen Sie alle .wav-Dateien hintereinander
for wav_file in wav_files:
    wav_path = os.path.join(processing_folder, wav_file)
    wav = wave.open(wav_path, "rb")
    combined_wav.writeframes(wav.readframes(wav.getnframes()))
    wav.close()

# Schließen Sie die kombinierte .wav-Datei
combined_wav.close()

print("Alle .wav-Dateien wurden zu einer Datei kombiniert und gespeichert.")