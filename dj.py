import alsaaudio
import numpy as np
import pyaudio
import tkinter as tk

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

m = alsaaudio.Mixer()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

top = tk.Toplevel(root)
top.attributes("-fullscreen", True)
top.configure(background="white")

alpha = 0.35

smoothed_bass_level = 0

while True:
    data = np.fromstring(stream.read(1024), dtype=np.int16)

    fft_data = np.fft.rfft(data)

    freq = np.fft.rfftfreq(1024, 1.0 / 44100)
    bass_indexes = np.where((freq >= 60) & (freq <= 150))[0]
    bass_magnitudes = np.abs(fft_data[bass_indexes])

    max_bass_level = np.max(bass_magnitudes)

    normalized_bass_level = (max_bass_level - 1000000) / 2300000

    smoothed_bass_level = alpha * normalized_bass_level + (1 - alpha) * smoothed_bass_level

    top.attributes("-alpha", smoothed_bass_level)

    root.update_idletasks()
    top.update()
