import random
import threading


def runnable(par):
    for i in range(10 ** 7):
        if random.random() < 10 ** -6:
            print(7)


class Main:
    def __init__(self):
        t = threading.Thread(target=runnable, args=(self,))
        t.start()
        for _ in range(10 ** 7):
            if random.random() < 10 ** -6:
                print(8)
        t.join()

    def dummy(self):
        input(">")
        return 7


if __name__ == '__main__':

    Main()
