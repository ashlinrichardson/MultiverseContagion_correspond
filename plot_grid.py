import os
import sys
import matplotlib.pyplot as plt
sep = os.path.sep

T = 2000.
means = [x.strip() for x in os.popen('find ./ -name "mean.csv"')]

dirs = [sep.join(x.split(sep)[:-1]) + sep for x in means]
sirs = [x + "sir.csv" for x in dirs]
bgr = [x + "beta_gamma_R0.csv" for x in dirs] # beta gamma r0 files..

curves = []
for ix in range(len(means)):
    m = means[ix]
    d = dirs[ix]
    print(ix, d)
    a = os.system("python3 fit_sir.py " + d)

    x = [i.strip() for i in open(m).readlines()]
    x = [float(i) for i in x]
    if len(x) < 1:
        continue
    last = x[-1]
    while len(x) < T:
        x += [last]
    print(len(x), x)

    plt.plot(x)
plt.tight_layout()
plt.savefig("grid1000.png")
