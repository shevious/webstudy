import numpy as np
import matplotlib.pyplot as plt

def generator(data, lookback, delay, min_index, max_index,
              shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(
                min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)

        samples = np.zeros((len(rows),
                           lookback // step,
                           data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets

def create_sine():
    n = 1000
    offset = 0
    i = np.arange(0, n)
    x = i*10*np.pi/n
    y = np.sin(x)
    z = np.sign(y)
    data = np.dstack((y,z))
    #plt.plot(i, y)
    #plt.show()
    return data

data = create_sine()
total_no = len(data)
valsplit = 0.3
max_index = int((1-valsplit)*total_no)

train_gen = generator(data, lookback=100, delay=10, min_index=0, max_index=max_index)

