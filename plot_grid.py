'''NB don't forget to pull the SIR data out of here: e.g.
  +w 500_0.6_1.3_1.1_9.4_5_1/sir.csv

..and truncate both to the simulation length generated. 

ideally we would be fitting on this length of curve as well.. leave that shortcoming for now'''

import os
import sys
import matplotlib.pyplot as plt
sep = os.path.sep

T = 500 # was 2000 # pad up to this time, if insufficient data.. Or truncate after this time.. If sufficient data
means = [x.strip() for x in os.popen('find ./ -name "mean.csv"')]

dirs = [sep.join(x.split(sep)[:-1]) + sep for x in means] # simulation-batch folders (one per batch)..
sirs = [x + "sir.csv" for x in dirs]  # SIR curve data, fit to mean of a batch (one folder per batch above..)
bgr = [x + "beta_gamma_R0.csv" for x in dirs] # beta gamma r0 files.. for each SIR fit


f = open("data.dat", "wb")
f.write(("HzR,sizeF,mF,beta,gamma,R0,n_covid_sim,n_sir_fit\n").encode())
curves = []
for ix in range(len(means)):
    m = means[ix]
    d = dirs[ix]
    sir = sirs[ix]
    print("*", ix, d)

    dp = d.strip().strip(".").strip(sep)
    w = dp.split("_")
    
    HzR = float(w[1])
    sizeF = float(w[2])
    mF = float(w[3])

    if not os.path.exists(bgr[ix]):
        print("+w", bgr[ix])
        a = os.system("python3 fit_sir.py " + d)

    print("+r", bgr[ix])
    beta, gamma, R0 = [float(j) for j in open(bgr[ix]).read().strip().split(",")]

    x = [i.strip() for i in open(m).readlines()]
    x = [float(i) for i in x]

    if len(x) < 1:
        continue
    
    last = x[-1]
    while len(x) < T:
        x += [last]

    if len(x) > T:
        x = x[0: T]

    # print(len(x), x)

    plt.plot(x)

    sir_c = [float(x) for x in open(sir).read().strip().split("\n")]
    last = sir_c[-1]
    while len(sir_c) < T:
        sir_c += [last]
    if len(sir_c) > T:
        sir_c = sir_c[0: T]

    f.write((",".join([str(HzR), str(sizeF), str(mF)] + [str(beta), str(gamma), str(R0)] + [str(len(x)), str(len(sir_c))] + [str(xi) for xi in x] + [str(xi) for xi in sir_c]) + "\n").encode())
plt.tight_layout()
plt.savefig("grid1000.png")
f.close()
