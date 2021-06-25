'''
this one should be run after write_csv_run_grid.py
'''
import os
import sys
import numpy as np
import matplotlib as mp
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 9}
mp.rc('font', **font)
COLOR = 'white'
mp.rcParams['text.color'] = COLOR
mp.rcParams['axes.labelcolor'] = COLOR
mp.rcParams['xtick.color'] = COLOR
mp.rcParams['ytick.color'] = COLOR

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

if False:
    X = np.array([x for x in curve])
    print("fitting..")
    X_embedded = TSNE(n_components=2).fit_transform(X)

    print(X_embedded.shape)
    plt.plot(X_embedded)
    plt.tight_layout()
    plt.savefig("tsne_2d_curve.png")

if False:
    dx = [covid[i] + sirps[i] for i in range(len(covid))]
    X = np.array(dx)
    Xe= TSNE(n_components=2).fit_transform(X)
    plt.plot(Xe)
    plt.tight_layout()
    plt.savefig("tnse_2d_params.png")

if True:
    dx = [covid[i] + sirps[i] for i in range(len(covid))]
    X = np.array(dx)
    X = TSNE(n_components=3).fit_transform(X)
    print(X.shape)
    n = X.shape[0]
    N = range(n)
    rgb = [sirps[i] for i in N]
    r_min = min(np.array([sirps[i][0] for i in N]))
    r_max = max(np.array([sirps[i][0] for i in N]))
    g_min = min(np.array([sirps[i][1] for i in N]))
    g_max = max(np.array([sirps[i][1] for i in N]))
    b_min = min(np.array([sirps[i][2] for i in N]))
    b_max = max(np.array([sirps[i][2] for i in N]))
    rgb = [[(rgb[i][0] - r_min) / (r_max - r_min), 
            (rgb[i][1] - g_min) / (g_max - g_min), 
            (rgb[i][2] - b_min) / (b_max - b_min)] for i in N]

    from matplotlib import animation
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(16, 9), tight_layout=True, dpi=300)
    ax = None
    plt.rcParams['axes.facecolor'] = 'black'

    def init():
        global ax
        ax = plt.axes(projection='3d')
        ax.set_facecolor('black')
        ax.scatter3D(X[:, 0], X[:, 1], X[:, 2], c=rgb) # cmap='Greens')
        return fig,

    
    TF = 10  # time scaling factor
    # rotate the axes and update
    # for angle in range(0, 360):
    n_frames = 360 * TF
    def animate(i):
        ax.set_title("tSNE 3d proj. of (HzR, sizeF, mF, beta, gamma, R0).." +
                     "r,g,b= (beta, gamma, R0)")  
        print("render " + str(i) + " / " + str(n_frames))
        j = i / TF
        ax.view_init(45 - j/(TF / 2.5), j) # angle)
        return fig,
        #plt.pause(.001)
    
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=0, blit=True)
    anim.save('tSNE_vid_' + str(TF) + '_.mp4', fps=60, extra_args=['-vcodec', 'libx264'])
    # plt.tight_layout()
    # plt.savefig("tnse_2d_params.png")
