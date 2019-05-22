import numpy as np


class Objective(object):
    def __call__(self, x):
        return (x-15)**2

    def grad(self, x):
        return 2*x
