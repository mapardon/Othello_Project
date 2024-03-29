import random
import numpy as np
from src.game.Player import Player

# Activation functions #

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_gradient(x):
    return x * (1 - x)


def hyperbolic_tangent(x):
    return np.tanh(x)


def h_tangent_gradient(x):
    return 1 / np.power(np.cosh(x), 2)


def relu(x):
    return x * (x > 0)


def relu_gradient(x):
    return 1 * (x > 0)


class PlayerML(Player):

    def __init__(self, mode, role, network, game_parameters):
        """ ML agent for the game, using ML methods to play and learn the game and update weights (ideally, some methods
        would have been declared private but we do with what we have).

        :param mode: tells which mode is being played (match, train or compare) to know which attributes must be
        initialized
        :param role: important because whole implementation is considered from the point of view of white player,
        knowing we play the blacks imply we must search the least advantageous move.
        :param network: in train mode, both agents must share same NN object, so weights are read from GameEngine
        :param game_parameters: parameters collected from the UI, used to initialize agent """

        super().__init__(role)

        # process game_parameters from gui and initialize adequate variables
        self.network = network
        self.eps = game_parameters["eps"]
        self.act_f, self.grad = {"sigmoïd": (sigmoid, sigmoid_gradient),
                                 "hyperbolic tangent": (hyperbolic_tangent, h_tangent_gradient),
                                 "relu": (relu, relu_gradient)}[game_parameters["act_f"]]

        if mode == "train":
            self.ls = game_parameters["ls"]
            self.lr = game_parameters["lr"]
            self.mv_selec = game_parameters["mv_selec"]

        else:
            self.ls = self.lr = self.mv_selec = None

    # Communication with game loop #

    def make_move(self, game):
        """ Format game states then call adequate function to choose a move (and eventually learn)

        :returns None if no play is available """

        moves = [game.to_array(m) for m in game.playable_moves(self.role)]
        if not len(moves):
            return None

        if self.ls is None:
            return self.match_move(moves)

        elif self.ls == "Q-learning" or self.ls == "SARSA":  # Move + update weight matrices
            return self.learning_move(moves, game.to_array(None))

    def end_game(self, board, white_victory):
        """ Same as previous for the end of the game """

        if self.ls == "Q-learning" or self.ls == "SARSA":
            self.end_game_update(board.to_array(None), white_victory)

    # Moves ranking #

    def best_moves(self, moves):
        """ Search best moves among possibilities for epsilon-greedy
        :returns tuple containing:
                * list of the moves evaluated as most promising by the network
                * the probability estimation. """

        best_moves = list()
        best_value = None
        c = 1 if self.role else -1  # game is viewed under 2nd player pov

        for m in moves:
            estimation = self.forward_pass(m)
            if best_value is None or c * estimation > c * best_value:  # black move, invert inequality
                best_moves = [m]
                best_value = estimation
            elif estimation == best_value:
                best_moves.append(m)

        return best_moves, best_value

    def softmax_exponential(self, moves):
        """ Compute the softmax values for current possible moves. """

        if not self.role:
            x = np.array([1 - self.forward_pass(m) for m in moves])  # black player, complement probabilities
        else:
            x = np.array([self.forward_pass(m) for m in moves])

        return np.exp(x) / np.sum(np.exp(x), axis=0)

    # AI algorithms, training and move selection #

    def forward_pass(self, state):
        """ Use the knowledge of the network to make an estimation of the victory probability of the white (2nd) player
        of a provided game state. """

        W_int = self.network[0]
        W_out = self.network[1]
        P_int = self.act_f(np.dot(W_int, state))
        p_out = self.act_f(P_int.dot(W_out))  # output, estimation of the probability
        return p_out

    def match_move(self, moves):
        """ Non learning move, just make a choice among best known moves or randomly (epsilon-greedy). """

        if random.random() >= self.eps:  # Greedy, return best move
            return random.choice(self.best_moves(moves)[0])
        else:
            return random.choice(moves)

    def backpropagation(self, state, delta):
        """ Update weights of neural network with regard to the learning strategy and the activation function.

        :param state: current game state
        :param delta: difference of victory probability estimation between current state and next selected state """

        W_int = self.network[0]
        W_out = self.network[1]
        P_int = self.act_f(np.dot(W_int, state))
        p_out = self.act_f(P_int.dot(W_out))
        grad_out = self.grad(p_out)
        grad_int = self.grad(P_int)
        Delta_int = grad_out * W_out * grad_int

        W_int -= self.lr * delta * np.outer(Delta_int, state)
        W_out -= self.lr * delta * grad_out * P_int

    def learning_move(self, moves, state):
        """ Selects a move (either randomly or using the estimation provided by the network) and perform update of
        weights. """

        if self.mv_selec == "eps-greedy":
            best_moves, best_p_out = self.best_moves(moves)
            if random.random() > self.eps:  # Choose move among highest evaluated
                new_s = random.choice(best_moves)
            else:
                new_s = random.choice(moves)

        else:  # self.mv_selec == "softmax":
            softmax_vals = self.softmax_exponential(moves)
            new_s = moves[np.random.choice([i for i in range(len(moves))], p=softmax_vals)]
            best_p_out = self.forward_pass(moves[np.argmax(softmax_vals)])

        # Update NN weights
        if self.ls == "Q-learning":
            cmp_p_out = best_p_out
        else:  # self.ls == "SARSA":
            cmp_p_out = self.forward_pass(new_s)

        cur_p_out = self.forward_pass(state)
        delta = cur_p_out - cmp_p_out
        self.backpropagation(state, delta)

        return new_s

    def end_game_update(self, state, won):
        """ Called at the end of the game to perform one last update of weights with a certitude of the victory or
        defeat. """

        p_out_s = self.forward_pass(state)
        delta = p_out_s - won
        self.backpropagation(state, delta)
