import cupy as cp
import numpy as np
 
n_elements = 10 ** 7
arr_host = np.random.normal(size=n_elements)

# Compute the mean of the array `arr_host` on the GPU and name it `mean_dev`
# YOUR CODE HERE

# On the GPU: subtract the mean (computed above) from each element
# and square the result, naming the resulting array `squared_deviations_dev`
# YOUR CODE HERE

# On the GPU: calculate the average sum of squares (i.e. the average of `squared_deviations_dev`)
# and name it `variance_dev` (this is the population variance!)
# YOUR CODE HERE

# Send the mean and variance back to the CPU Host so that they can be printed below
# use variable names `mean_host` and `variance_host`
# YOUR CODE HERE

print(f"Mean: {mean_host}, Variance: {variance_host}")