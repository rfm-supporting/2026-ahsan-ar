import numpy as np

def f(x):
    x = np.array(x)
    y = np.empty(x.shape)
    i = x > (24/116) ** 3
    y[i]  = x[i] ** (1/3)
    y[~i] = (841/108) * x[~i] + (16/116)
    return y

def finv(y):
    y = np.array(y)
    x = np.empty(y.shape)
    i = y > ((841/108)*(24/116) ** 3) + (16/116)
    x[i] = y[i] ** 3
    x[~i] = (y[~i] - (16/116)) / (841/108)
    return x

def ref2mun(r):
    return (116 * f(r) - 16)/10

def mun2ref(m):
    return finv((10 * m + 16) / 116)
