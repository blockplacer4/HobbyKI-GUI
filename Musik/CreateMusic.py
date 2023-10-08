import wave
import os
import librosa
import soundfile as sf
import pyttsx3
import time
import threading
import pyaudio
import numpy as np
import random
pitch_pattern = []

input_wav_path = "gesprochen.wav"
stop_thread = False

def create_a_song(text):
    global stop_thread
    stop_thread = False
    def generate_melody(length):
    # Liste der verfügbaren Melodiemuster
        melodie_muster = ["JumpDown", "JumpUp", "Up", "Straight", "Down"]
        pitch_pattern = []
        x = 1
        # Erzeugen Sie die Melodie als zufällige Abfolge von Mustern
        melody = [random.choice(melodie_muster) for _ in range(length)]
        for i in melody:
            if i == "JumpDown":
                x -= 3
            elif i == "JumpUp":
                x += 3
            elif i == "Up":
                for _ in range(2):
                    x+= 1
                    pitch_pattern.append(x)
                x+=1
            elif i == "Down":
                for _ in range(2):
                    x-= 1
                    pitch_pattern.append(x)
                x -= 1
            elif i == "Straight":
                pass
            if x <= -20:
                x += 10
            elif x >= 20:
                x -= 10
            pitch_pattern.append(x)
        return pitch_pattern
    pitch_pattern = generate_melody(150)



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
    segment_laenge_s = 0.2

    # Erstellen Sie den Ordner "Processing", falls er nicht existiert
    output_folder = "Processing"
    os.makedirs(output_folder, exist_ok=True)

    # Lesen Sie die WAV-Daten
    wav_data = input_wav.readframes(num_frames)

    # Schließen Sie die Eingabe-WAV-Datei
    input_wav.close()

    # Konvertieren Sie die WAV-Daten in ein NumPy-Array
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

        # Wenden Sie das Pitch-Muster auf das Segment an
        pitch(output_wav_path, pitch_pattern[i % len(pitch_pattern)])

    print(f"{i+1} Sekundenabschnitte wurden im Ordner 'Processing' gespeichert und die Tonhöhe wurde geändert.")
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
    def play_wav_1(file_name):
    # Verwenden Sie die globale Variable
        global stop_thread

        wf = wave.open(file_name, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while not stop_thread:
            
            scaled_data = bytes([int(sample * 1) for sample in data])
            stream.write(scaled_data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()

        p.terminate()

    def play_wav_2(file_name):
        # Verwenden Sie die globale Variable
        global stop_thread

        wf = wave.open(file_name, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while data:
            scaled_data = bytes([int(sample * 1) for sample in data])
            stream.write(scaled_data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()

        p.terminate()
        
        # Set stop_thread to True after playback
        stop_thread = True  # Use global variabl


    # Dateinamen Ihrer WAV-Dateien
    file1 = 'input.wav'
    file2 = 'combined_audio.wav'  # Ändern Sie dies in den Dateinamen Ihrer zweiten WAV-Datei

    # Erstellen Sie einen Thread für die Wiedergabe der ersten WAV-Datei
    thread1 = threading.Thread(target=play_wav_1, args=(file1,))

    # Starten Sie den Thread
    thread1.start()

    # Warten Sie 4 Sekunden, bevor Sie den zweiten Thread starten
    time.sleep(4)

    # Erstellen Sie einen Thread für die Wiedergabe der zweiten WAV-Datei
    thread2 = threading.Thread(target=play_wav_2, args=(file2,))
    thread2.start()
    thread1.join()
    thread2.join()

    print("Threads wurden beendet")
create_a_song("Ist das eine Melodie?")
