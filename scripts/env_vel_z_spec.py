import json
import numpy as np

from scipy import signal
from scipy.fft import fft
from scipy.signal import hilbert

def vel_calc(time_series, sample_rate):
    time_series = time_series - np.mean(time_series)
    vel = []
    vel_tmp = 0
    for i in range(0, len(time_series)):
        vel_tmp = vel_tmp + time_series[i] / sample_rate
        vel.append(vel_tmp)
    return vel

def envelope(signal):
    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)
    amplitude_envelope = amplitude_envelope.tolist()
    return amplitude_envelope

def generate_spec_plot(file_path, toLog):
    f = open(file_path)
    data = json.load(f)
    sample_rate = data["sample_rate"]
    N = data["number_of_samples"]  # pobieramy ilość próbek z pliku

    #  -------------- MOZLIWOSC ZMIANY CZYTANEJ OSI --------------
    time_series = data["vibrationsZ"]
    time_series = time_series - np.mean(time_series)
    y1 = vel_calc(time_series, sample_rate)
    y1 = y1 - np.mean(y1)

    if(toLog):
        new=[]
        for val in y1:
            if(val<0):
                new.append(1)
            else:
                new.append(val)
                
        y1=np.log(new)

    yf1 = abs(fft(y1)) / N
    yf1 = envelope(yf1)
    f, t, Sxx = signal.spectrogram(y1, sample_rate)
    # f i t osie podpisy osiw szerokość / br  amplitusa

    main_y_list = []

    for i in range(0, len(yf1)):
        main_y_list.append(yf1[i])

    for i in range(0, 15):
        main_y_list[i] = 0
    for i in range(len(main_y_list) - 15, len(main_y_list)):
        main_y_list[i] = 0

    return {
        "Heatmap": {
            "z": Sxx.T.tolist(),
            "x": f.tolist(),
            "y": t.tolist()
        }
    }
