import os
import sys
import matplotlib.pyplot as plt
sep = os.path.sep

T = 500. # was 2000
means = [x.strip() for x in os.popen('find ./ -name "mean.csv"')]

dirs = [sep.join(x.split(sep)[:-1]) + sep for x in means]
sirs = [x + "sir.csv" for x in dirs]
bgr = [x + "beta_gamma_R0.csv" for x in dirs] # beta gamma r0 files..


f = open("data.dat", "wb")
f.write(("HzR,sizeF,mF,beta,gamma,R0\n").encode())
curves = []
for ix in range(len(means)):
    m = means[ix]
    d = dirs[ix]
    print("*", ix, d)

    dp = d.strip().strip(".").strip(sep)
    w = dp.split("_")
    
    HzR = float(w[1])
    sizeF = float(w[2])
    mF = float(w[3])

    if not os.path.exists(bgr[ix]):
        a = os.system("python3 fit_sir.py " + d)

    beta, gamma, R0 = [float(j) for j in open(bgr[ix]).read().strip().split(",")]

    x = [i.strip() for i in open(m).readlines()]
    x = [float(i) for i in x]
    if len(x) < 1:
        continue
    last = x[-1]
    while len(x) < T:
        x += [last]
    # print(len(x), x)

    plt.plot(x)

    f.write((",".join([str(HzR), str(sizeF), str(mF)] + [str(beta), str(gamma), str(R0)] + [str(xi) for xi in x]) + "\n").encode())
plt.tight_layout()
plt.savefig("grid1000.png")
f.close()
