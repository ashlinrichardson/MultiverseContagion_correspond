import os
import sys
import matplotlib.pyplot as plt

T = 2000.
means = [x.strip() for x in os.popen('find ./ -name "mean.csv"')]

curves = []
for m in means:
    x = [i.strip() for i in open(m).readlines()]
    x = [float(i) for i in x]
    if len(x) < 1:
        continue
    last = x[-1]
    while len(x) < T:
        x += [last]
    print(len(x))

    plt.plot(x)
plt.tight_layout()
plt.show()
