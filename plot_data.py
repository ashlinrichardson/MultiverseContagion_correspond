import os
import sys
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

lines = [x.strip() for x in open("data.dat").readlines()]

curve = []
covid = []
sirps = []
ci = 0
for line in lines:
    ci += 1
    if ci ==1:
        continue
    w = line.split(",")

    csi = [float(x) for x in w[0:3]]
    sir = [float(x) for x in w[3:6]]
    cur = [float(x) for x in w[7:]]

    curve.append(cur)
    covid.append(csi)
    sirps.append(sir)

if True:
    X = np.array([x for x in curve])
    print("fitting..")
    X_embedded = TSNE(n_components=2).fit_transform(X)

    print(X_embedded.shape)
    plt.plot(X_embedded)
    plt.tight_layout()
    plt.show()



if False:
    dx = [covid[i] + sirps[i] for i in range(len(covid))]
    X = np.array(dx)
    Xe= TSNE(n_components=2).fit_transform(X)
    plt.plot(Xe)
    plt.tight_layout()
    plt.show()
