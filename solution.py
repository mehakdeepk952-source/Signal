import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import iirnotch, lfilter,butter


fs, signal = wavfile.read('corrupted.wav')
t = np.linspace(0, len(signal)/fs, len(signal))

plt.figure(figsize=(12, 5))
plt.plot(t, signal, color='blue')
plt.title(" Time Domain ")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.savefig('stage1_time_domain.png')
plt.show()

fft_data = np.fft.rfft(signal)
freqs = np.fft.rfftfreq(len(signal), 1/fs)
magnitude = np.abs(fft_data)

plt.figure(figsize=(12, 5))
plt.plot(freqs, magnitude, color='blue')
plt.title("Stage 1: FFT Plot")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (Energy)")
plt.grid(True)
plt.savefig('stage1_fft.png') 
plt.show()


peak_freq = freqs[np.argmax(magnitude)]
fc=7300.20
t = np.linspace(0, len(signal) / fs, len(signal))
new_signal=signal*np.cos(2*np.pi*fc*t)
fft_new = np.fft.rfft(new_signal)
freq_new=np.fft.rfftfreq(len(signal), 1/fs)
plt.figure(figsize=(12,5))
plt.plot(freq_new,np.abs(fft_new), color='green')
plt.title(f"Graph Shifted to Center (fc={fc} Hz)")
plt.xlabel("Frequency (Hz)")
plt.savefig('stage2_fft.png') 
plt.show()
peak_freq_new = freq_new[np.argmax(np.abs(fft_new))]

magnitude_stage3 = np.abs(np.fft.rfft(new_signal))
freqs_stage3 = np.fft.rfftfreq(len(new_signal), 1/fs)
threshold = np.mean(magnitude_stage3) * 5
spikes = freqs_stage3[magnitude_stage3 > threshold]
audible_spikes = [f for f in spikes if 50 < f < 4500]

def lowpass_filter(data, cutoff, fs, order=6):
    nyq = 0.5 * fs
    b, a = butter(order, cutoff/nyq, btype='low')
    return lfilter(b, a, data)

stage3_signal=lowpass_filter(new_signal, 4000, fs)
for i in audible_spikes:
    f_remove = i
    Q = 30.0 
    b, a = iirnotch(f_remove, Q, fs)
    stage3_signal = lfilter(b, a, stage3_signal)

fft_stage3 = np.fft.rfft(stage3_signal)
freq_stage3 = np.fft.rfftfreq(len(stage3_signal), 1/fs)
magnitude_stage3 = np.abs(fft_stage3)
plt.figure(figsize=(12, 5))
plt.plot(freq_stage3, magnitude_stage3, color='purple')


plt.title("Graph Filtering")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)

plt.savefig('stage3_fft.png')
plt.show()

final_recovered_audio = stage3_signal[::-1]


final_recovered_audio = final_recovered_audio / np.max(np.abs(final_recovered_audio))
output_filename = 'recovered.wav'
wavfile.write(output_filename, fs, (final_recovered_audio* 32767).astype(np.int16))

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(t, stage3_signal, color='purple', linewidth=0.5)
plt.title(" Before Time-Reversal ")
plt.ylabel("Amplitude")
plt.grid(True)

final_audio = stage3_signal[::-1] 
plt.subplot(2, 1, 2)
plt.plot(t, final_audio, color='pink', linewidth=0.5)
plt.title(" After Time-Reversal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.savefig('stage4.png')
plt.show()
