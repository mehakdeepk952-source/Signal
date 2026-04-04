# Signal
The project is based on undoing the changes done to a .wav file ,identify the corrupted signals and plot the FFT at each step.

The energy was concentrated in a high-frequency band centered around 7300 Hz.It was clear the signal had been modulated.
To bring the signal back to the baseband (0–4000 Hz), I multiplied the signal by a local oscillator (cosine wave) at the carrier frequency fc . This shifts the energy back to 0 Hz.
After shifting the signal, the FFT revealed several sharp, narrow spikes in the human ear audible range.
I applied a 6th-order Butterworth low-pass filter with a cutoff of 4000 Hz to remove the 2fc and notch filters to remove the spikes.
The audio remained unaudible. This suggested the final step was a Time Reversal.
I reversed the array indices of the signal to get the original audio.
