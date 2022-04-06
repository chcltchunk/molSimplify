""" A few utilities for Indian Buffet Processes. """

__author__ = 'Tom Schaul, tom@idsia.ch'


from scipy import zeros, rand, array, sqrt
from numpy.random import beta


def leftordered(M):
    """ Returns the given matrix in left-ordered-form. """
    l = list(M.T)
    l.sort(key=tuple)
    return array(l)[::-1].T


def generateIBP(customers, alpha=10, reducedprop=1.):
    """ Simple implementation of the Indian Buffet Process. Generates a binary matrix with
    customers rows and an expected number of columns of alpha * sum(1,1/2,...,1/customers).
    This implementation uses a stick-breaking construction.
    An additional parameter permits reducing the expected number of times a dish is tried. """
    # max number of dishes is distributed according to Poisson(alpha*sum(1/i))
    _lambda = alpha * sum(1. / array(range(1, customers + 1)))
    alpha /= reducedprop

    # we give it 2 standard deviations as cutoff
    maxdishes = int(_lambda + sqrt(_lambda) * 2) + 1

    res = zeros((customers, maxdishes), dtype=bool)
    stickprops = beta(alpha, 1, maxdishes) # nu_i

    currentstick = 1.
    dishesskipped = 0

    for i, nu in enumerate(stickprops):
        currentstick *= nu
        dishestaken = rand(customers) < currentstick * reducedprop
        if sum(dishestaken) > 0:
            res[:, i - dishesskipped] = dishestaken
        else:
            dishesskipped += 1

    return res[:, :maxdishes - dishesskipped]


def testIBP():
    """ Plot matrices generated by an IBP, for a few different settings. """

    from pybrain.tools.plotting.colormaps import ColorMap
    import pylab

    # always 50 customers
    n = 50

    # define parameter settings
    ps = [(10, 0.1),
          (10,), (50,),
          (50, 0.5),
          ]

    # generate a few matrices, on for each parameter setting
    ms = []
    for p in ps:
        if len(p) > 1:
            m = generateIBP(n, p[0], p[1])
        else:
            m = generateIBP(n, p[0])
        ms.append(leftordered(m))

    # plot the matrices
    for m in ms:
        ColorMap(m, pixelspervalue=3)
    pylab.show()


if __name__ == '__main__':
    testIBP()
