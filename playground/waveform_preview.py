from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

samplerate, data = wavfile.read('./recordings/code_vs_quote.wav')

pool_size = 100
data = data[:data.shape[0]//pool_size*pool_size]
data = data.reshape((-1, pool_size))
data_mean = np.mean(data, axis=1)
data_max = np.max(data, axis=1)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(data_mean)
ax2.plot(data_max)
plt.show()
