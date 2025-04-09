import numpy as np
import time

t0 = time.time()
# generate 1m simulation runs
N = 10 ** 6

# each random walk has 100 random normal steps
steps = np.random.normal(loc=0, scale=1, size=(N, 100))

# each walk starts at 100 and then diverges based on randomly generated steps
steps[:, 0] = 0
r_walks = 100 + np.cumsum(steps, axis=1)

average_finish = np.mean(r_walks[:, -1])
std_finish = np.std(r_walks[:, -1])
print(f'Average Finish: {average_finish}, Standard Deviation: {std_finish}')
t1 = time.time()
print(f'Time (s): {t1-t0}')
