import numpy as np
import scipy
from numpy.fft import fft, ifft


def resample(X, Y, sr):
    """
    resample a given set of signal (linear interpolation)
    :param X: X value of the signal (could be time)
    :param Y: value of the signal
    :param sr: sample rate
    :return: resample serie
    """
    tmin, tmax = min(X), max(X)
    f = scipy.interpolate.interp1d(X, Y, fill_value = "extrapolate")
    # Building resampled list
    x = np.arange(tmin, tmax, 1 / sr)
    y = np.array([f(t) for t in x])
    return x, y


def old_FFT(XX, YY, sr, norm=False):
    """
    Return frequence and amplitude from the FFT
    :param XX: x component of the signal (like time)
    :param YY: y component of the signal
    :param sr: sample rate
    :param norm: if amplitude is normalize to one or not
    :return:
    """
    x, y = resample(XX, YY, sr=sr)
    Y = fft(y)
    N = len(Y)
    n = np.arange(N)
    T = N / sr
    freq = n / T
    out = np.abs(Y)
    if norm:
        out = out / max(out)
    print(len(freq))
    return freq, out

def FFT(t, f, sr=None):
    """
    Return frequence and amplitude from the FFT
    :param t: time
    :param f: function
    :param sr: sample rate, if you need to resample

    :return:
    """
    if sr != None:
        t, f = resample(t, f, sr=sr)
    dt = 1/sr
    n = len(t)
    f_hat = fft(f,n)
    PSD = np.real(f_hat * np.conjugate(f_hat)/n)
    freq = (1/(dt*n))*np.arange(n)
    L= np.arange(1,np.floor(n/2), dtype = 'int') #remove continuous component
    freq_plot = freq[L]
    PSD_plot = PSD[L]
    return (PSD,freq,PSD_plot,freq_plot,f_hat,t)

def threshold_filter(f_hat,PSD, PSD_threshold):
    """
    Perform a threshold filter on a f_hat = FFT(f). Cut all frequencies with PSD<PSD_threshold
    :param f_hat: FFT(f)
    :param PSD_threshold: Threshold on the PSD of f_hat
    :return: filter f_hat, and f
    """
    indices = PSD>PSD_threshold
    PSD_out = PSD*indices
    f_hat = indices*f_hat
    return PSD_out,f_hat
