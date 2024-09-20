import alsaaudio
import numpy as np
import pyaudio
import tkinter as tk

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024
)

# Initialize ALSA Mixer
m = alsaaudio.Mixer()

# Initialize Tkinter
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

top = tk.Toplevel(root)
top.attributes("-fullscreen", True)
top.configure(background="white")

alpha = 0.35
smoothed_bass_level = 0

while True:
    # Read audio data
    data = np.frombuffer(stream.read(1024), dtype=np.int16)

    # Perform FFT
    fft_data = np.fft.rfft(data)

    # Extract bass frequencies
    freq = np.fft.rfftfreq(1024, 1.0 / 44100)
    bass_indexes = np.where((freq >= 60) & (freq <= 150))[0]
    bass_magnitudes = np.abs(fft_data[bass_indexes])

    # Calculate bass level
    max_bass_level = np.max(bass_magnitudes)
    normalized_bass_level = (max_bass_level - 1000000) / 2300000

    # Smooth the bass level
    smoothed_bass_level = (
        alpha * normalized_bass_level + (1 - alpha) * smoothed_bass_level
    )

    # Update Tkinter window transparency
    top.attributes("-alpha", smoothed_bass_level)

    # Update Tkinter GUI
    root.update_idletasks()
    top.update()
