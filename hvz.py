import sys
import math
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

pop_size = 500.
infected = 5.

fn = "mean.csv"
yd = [float(x.strip()) for x in open(fn).readlines()]
td = [float(x) for x in range(len(yd))]
td, yd = np.array(td), np.array(yd)
yd += infected # initial population needs to be added on
td += 1. # initial time from 1. to avoid math error

yd /= pop_size # divide by population
td /=float(len(td))

def fx(x, a, c1, c2):
    '''
    print("\tx=" + str(x))
    print("\ta=" + str(a))
    print("\tb=" + str(b))
    print("\tc=" + str(c))
    '''
    return c1 * np.power(a * c1 * x + c1 * c2, -1.) + c1

y0 = (yd[0] + infected / pop_size)
x0 = (pop_size - y0)  / pop_size
c1 = y0 - x0
c2 =  (1. / c1) * math.log(1. - c1 / x0)
a =  (1. / (y0 * td[-1])) * ( math.log( (y0 / (yd[-1] - y0)) + 1) - c2 * y0)

guess = [a, c1, c2]
print("guess a", a)
print("guess b=c1", c1)
print("guess c=c2", c2)

a =  -.1
c1 =  1.
c2 = -1

y = fx(td, a, c1, c2)
plt.plot(td, yd, color='b')
plt.plot(td, y, color='r')
plt.show()


popt, pcov = curve_fit(fx, td, yd, guess)

a, b, c = popt # a, c_1, c_2

print("a", a)
print("b", b)
print("c", c)

print("got here")


'''
a = -.001
b = - 5
c = -.01
'''
y = fx(td, a, b, c)

plt.plot(td,yd, color='b')
plt.plot(td, y, color='r')
plt.show()
