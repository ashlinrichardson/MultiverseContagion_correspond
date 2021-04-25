import os
import sys
import matplotlib.pyplot as plt
args = sys.argv

x, y = [], []
lines = open(args[1]).readlines()
lines = [x.strip() for x in lines]

for line in lines:
    w = line.split()
    yi, xi = w[0].strip('I'), w[7][3:]
    x.append(float(xi))
    y.append(float(yi))

plt.xlabel('gen')
plt.ylabel('INF')
plt.plot(x, y)
plt.savefig('plot.png')
