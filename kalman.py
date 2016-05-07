import math
class Kalman(object):

    """Docstring for Kalman. """

    def __init__(self, R=1, Q=1, A=1, B=0, C=1):
        """TODO: to be defined1. """
        self.R = R
        self.Q = Q
        self.A = A
        self.C = C
        self.B = B
        self.cov = float('nan')
        self.x = float('nan')

    def filter(self, z, u=0):
        """TODO: Docstring for filter.
        :returns: TODO

        """
        if(math.isnan(self.x)):
            self.x = (1 / self.C) * z
            self.cov = (1 / self.C) * self.Q * (1 / self.C)
        else:
            predX = (self.A * self.x) + (self.B * u)
            predCov = ((self.A * self.cov) * self.A) + self.R

            K = predCov * self.C * (1 / ((self.C * predCov * self.C) + self.Q))

            self.x = predX + K * (z - (self.C * predX))
            self.cov = predCov - (K * self.C * predCov)

        return self.x
