""" Define functions managing storage of neural networks (matrices weights) and other related info as the
activation function used with this network.

By default, "name" of a network will be used as key inside the shelve and

Schema of stored data:
    {"network_name": {"act_f": <name in str>, "w_int": <numpy 2d array>, "w_out"= <numpy 2d array>}, ...} """

import shelve

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


def save_new_network(network_name, act_f, w_int, w_out):
    """ Same as previous but used for newly created network so save activation function name as well """

    with shelve.open(STORAGE, writeback=True) as db:
        db[network_name] = dict()
        db[network_name]["act_f"], db[network_name]["w_int"], db[network_name]["w_out"] = act_f, w_int, w_out


def load_network(network_name):
    """ Retrieve stored weights and associated activation function """

    with shelve.open(STORAGE, writeback=True) as db:
        act_f, w_int, w_out = db[network_name]["act_f"], db[network_name]["w_int"], db[network_name]["w_out"]

    return act_f, w_int, w_out
