import matplotlib.pyplot as plt
import numpy as np      
import pyaudio as pa
def plot_waveform(waveform, sample_rate=44100):
    """
    Plots the waveform of an audio signal.
    
    Parameters:
    waveform (numpy.ndarray): The audio signal to plot.
    sample_rate (int): The sample rate of the audio signal.
    """
    plt.figure(figsize=(12, 4))
    time = np.arange(len(waveform)) / sample_rate
    plt.plot(time, waveform)
    plt.title('Waveform')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()
    plt.show(block=False)
    UnicodeTranslateError
    