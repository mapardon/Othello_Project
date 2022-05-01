""" Define functions managing storage of neural networks (matrices weights) and other related info as the
activation function used with this network.

By default, the "name" of a network will be used as key inside the shelve.

Schema of stored data:
    {"network_name": {"ls": <learning strategy>, "act_f": <name in str>, "w_int": <numpy 2d array>,
    "w_out"= <numpy 2d array>}, ...} """

import shelve

import numpy as np

STORAGE = "./db/stored-networks"


def available_networks():
    """ Return list of names of stored networks """

    networks = list()
    with shelve.open(STORAGE) as db:

        for k in db.keys():
            networks.append(k)

    return networks


def update_network(network_name, w_int, w_out):
    """ Update weight matrices of a stored network (after training)

    :param network_name: name of the network, identifying key inside the shelve
    :param w_int: weights between input & hidden layer
    :param w_out: weights between hidden layer and ouput """

    with shelve.open(STORAGE, writeback=True) as db:
        db[network_name]["w_int"], db[network_name]["w_out"] = w_int, w_out


def save_new_network(network_name, ls, act_f, n_input, n_hidden):
    """ Same as previous but applied to new network so requires activation function and learning strategy and perform
    initialization of matrices first.
    """

    w_int = np.random.normal(0, 0.0001, (n_hidden, n_input))
    w_out = np.random.normal(0, 0.0001, (n_hidden, 1))[:, 0]
    # W2 is considered as a vector and not input_size x 1 matrix to simplify some notations

    with shelve.open(STORAGE, writeback=True) as db:
        db[network_name] = dict()
        db[network_name]["ls"], db[network_name]["act_f"], db[network_name]["w_int"], db[network_name]["w_out"] = \
            ls, act_f, w_int, w_out


def load_network(network_name):
    """ Retrieve stored weights and associated activation function """

    with shelve.open(STORAGE, writeback=True) as db:
        ls, act_f, w_int, w_out = db[network_name]["ls"], db[network_name]["act_f"], db[network_name]["w_int"], db[network_name]["w_out"]

    return ls, act_f, w_int, w_out


def remove_network(name):

    with shelve.open(STORAGE, writeback=True) as db:
        del db[name]
