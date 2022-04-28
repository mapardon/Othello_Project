import random
import numpy as np
from game.Player import Player


# Activation functions #

def sigmoid(x):
    """ Possible activation function. """
    return 1 / (1 + np.exp(-x))


def sigmoid_gradient(x):
    """ Derivative of the sigmoid """
    return x * (1 - x)


def hyperbolic_tangent(x):
    return np.tanh(x)


def h_tangent_gradient(x):
    return 1 / np.power(np.cosh(x), 2)


def relu(x):
    return x * (x > 0)


def relu_gradient(x):
    return (x > 0) * 1


class PlayerML(Player):

    def __init__(self, mode, role, network, game_parameters):
        """ ML agent for the game, using ML methods to play and learn the game and update weights (ideally, some methods
        would have been declared private but we do with what we have).

        :param mode: tells which mode is being played (match, train or compare) to know which attributes must be
        initialized
        :param role: important because whole implementation is considered from the point of view of white player,
        knowing we play the whites implies we must search the least advantageous move.
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
            self.eps_dec = game_parameters["eps_dec"]
            print("Agent {} parameters:\n   eps: {}\n   ls: {}\n   lr: {}\n   eps_dec: {}\n   act fun: {}".format(
                self.role, self.eps, self.ls, self.lr, self.eps_dec, game_parameters["act_f"]))

        else:
            self.ls = self.lr = self.eps_dec = None
            print("Agent {} parameters:\n   eps: {}".format(self.role, self.eps))

    # Communication with game loop #

    def make_move(self, game):
        """ Format game states then call ai compute_move functions

        :returns None if no play is available """

        ops = game.playable_moves(self.role)
        if not len(ops):
            return None

        return self.compute_move([game.to_array(b) for b in ops], game.to_array(None))

    def end_game(self, board, victory):
        self.endGame(board.to_array(None), victory)

    # AI algorithms, training and choosing move #

    def forwardPass(self, s):
        """Cette fonction permet d'utiliser un réseau de neurones NN pour estimer la probabilité de victoire finale du
        joueur blanc pour un état (:param s) donné du jeu. """
        W_int = self.network[0]
        W_out = self.network[1]
        P_int = self.act_f(np.dot(W_int, s))
        p_out = self.act_f(P_int.dot(W_out))
        return p_out

    def backpropagation(self, s, delta):
        """Fonction destinée à réaliser la mise à jour des poids d'un réseau de neurones (NN). Cette mise à jour se fait
        conformément à une stratégie d'apprentissage (learning_strategy) pour un état donné (s) du jeu. Le delta est la
        différence de probabilité de gain estimée entre deux états successif potentiels du jeu. La stratégie
        d'apprentissage peut soit être None, soit il s'agit d'un tuple de la forme ('Q-learning', alpha) où alpha est le
        learning_rate (une valeur entre 0 et 1 inclus), soit il s'agit d'un tuple de la forme ('TD-lambda', alpha, lamb,
        Z_int, Z_out) où alpha est le learning_rate, lamb est la valeur de lambda (entre 0 et 1 inclus) et Z_int et Z_out
        contiennent les valeurs de l'éligibility trace associées respectivement aux différents poids du réseau de
        neurones. La fonction de backpropagation ne retourne rien de particulier (None) mais les poids du réseau de
        neurone NN (W_int, W_out) peuvent être modifiés, idem pour l'eligibility trace (Z_int et Z_out) dans le cas où la
        stratégie TD-lambda est utilisée.
        """

        if self.ls is not None:
            W_int = self.network[0]
            W_out = self.network[1]
            P_int = self.act_f(np.dot(W_int, s))
            p_out = self.act_f(P_int.dot(W_out))
            grad_out = self.grad(p_out)
            grad_int = self.grad(P_int)
            Delta_int = grad_out * W_out * grad_int

            if self.ls == 'Q-learning':
                W_int -= self.lr * delta * np.outer(Delta_int, s)
                W_out -= self.lr * delta * grad_out * P_int

            # TODO if we use it
            """
            elif self.ls[0] == 'TD-lambda':
                alpha = learning_strategy[1]
                lamb = learning_strategy[2]
                Z_int = learning_strategy[3]
                Z_out = learning_strategy[4]
                Z_int *= lamb
                Z_int += np.outer(Delta_int, s)
                Z_out *= lamb
                Z_out += grad_out * P_int
                W_int -= alpha * delta * Z_int
                W_out -= alpha * delta * Z_out
            """

    def compute_move(self, moves, state):
        """Fonction appelée pour que l'IA choisisse une action (le nouvel état new_s est retourné) à partir d'une liste
        d'actions possibles "moves" (c'est-à-dire une liste possible d'états accessibles) à partir d'un état actuel (s)
        Un réseau de neurones (NN) est nécessaire pour faire ce choix quand le mouvement n'est pas du hasard. Dans le cas
        greedy (non aléatoire), la couleur du joueur dont c'est le tour sera utilisée pour déterminer s'il faut retenir
        le meilleur ou le pire coup du point de vue du joueur blanc. Le cas greedy survient avec une probabilité 1-eps.
        La stratégie d'apprentissage fait référence à la stratégie utilisée dans la fonction de backpropagation (cfr la
        fonction de backpropagation pour une description)
        color : 0 = black player ; 1 = white player. We consider game under same pov, we juste inverted color convention.
        """
        q_learning = self.ls == "Q-learning"
        TD_lambda = self.ls == "TD-lambda"
        # Epsilon greedy
        greedy = random.random() > self.eps
        # dans le cas greedy, on recherche le meilleur mouvement (état) possible. Dans le cas du Q-learning (même sans
        # greedy), on a besoin de connaître la probabilité estimée associée au meilleur mouvement (état) possible en vue
        # de réaliser la backpropagation.

        if greedy or q_learning:
            best_moves = []
            best_value = None
            c = 1 if self.role else -1  # game is viewed under 2nd player pov
            for m in moves:
                val = self.forwardPass(m)
                if best_value is None or c * val > c * best_value:  # black move, invert inequality
                    best_moves = [m]
                    best_value = val
                elif val == best_value:
                    best_moves.append(m)

        if greedy:
            # Choose move among highest evaluated (if several of them, otherwise it's a 1 choose 1 choice)
            new_s = random.choice(best_moves)
        else:
            new_s = random.choice(moves)

        # Update NN weights if necessary
        if q_learning or TD_lambda:
            p_out_s = self.forwardPass(state)
            if q_learning:
                delta = p_out_s - best_value
            elif TD_lambda:
                if greedy:
                    p_out_new_s = best_value
                else:
                    p_out_new_s = self.forwardPass(new_s)
                delta = p_out_s - p_out_new_s
            self.backpropagation(state, delta)

        return new_s

    def endGame(self, s, won):
        """Cette fonction est appelée en fin de partie, pour une dernière mise à jour des poids lorsqu'une stratégie
        d'apprentissage est appliquée. Les arguments s, NN et learning strategy sont les mêmes que ceux de la fonction
        make_move() décrite ci-dessus. Ce qui change, c'est le booléen "won" indiquant si le joueur blanc a gagné (True)
        ou perdu (False). On est ici certain de la probabilité de gain de blanc (1 ou 0). Comme précédemment,
        si une stratégie d'apprentissage est appliquée, un delta sera calculé : ce sera ici sur la base de la probabilité
        associée au dernier état et de la conséquence associée (victoire ou défaite de blanc). Il servira à la mise à
        jour des poids du réseau de neurones. Dans le cas du TD-lambda, les éligibility traces sont aussi remises à 0 à
        la fin. Donc, cette fonction ne retourne rien (None) mais elle peut avoir un impact sur les valeurs des poids de
        NN et sur l'eligibility trace associée (quand TD-lambda est utilisée)
        """

        if self.ls in ["Q-learning"]:
            p_out_s = self.forwardPass(s)
            delta = p_out_s - won
            self.backpropagation(s, delta)

            if self.ls == "TD-lambda":
                # on remet les eligibility traces à 0 en prévision de la partie suivante
                self.ls[3].fill(0)  # remet Z_int à 0
                self.ls[4].fill(0)  # remet Z_out à 0
