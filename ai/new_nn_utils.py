""" Operations for creating and initializing new neural network """

import numpy as np


def create_NN(n_input, n_hidden):
    """ Create new neural network of required size (depends on input size and number of hidden neurons) and initialize
    with small random numbers. Network is returned as a tuple of two numpy array (for now, we consider only 1 hidden
    layer). """

    W_int = np.random.normal(0, 0.0001, (n_hidden, n_input))
    W_out = np.random.normal(0, 0.0001, (n_hidden, 1))[:, 0]
    # W2 is considered as a vector and not input_size x 1 matrix to simplify some notations
    return W_int, W_out
