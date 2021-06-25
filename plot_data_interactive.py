'''this one should be run after write_csv_run_grid.py
.. should have a switch between video and interactive mode!'''

INTERACTIVE_MODE = True
ANIMATION_MODE = not INTERACTIVE_MODE # disable user input to plot a video!

import os
import sys
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib import animation
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 7}
mp.rc('font', **font)
COLOR = 'white' if ANIMATION_MODE else 'black'
mp.rcParams['text.color'] = COLOR
mp.rcParams['axes.labelcolor'] = COLOR
mp.rcParams['xtick.color'] = COLOR
mp.rcParams['ytick.color'] = COLOR

# lines = [x.strip() for x in open("data.dat").readlines()]
lines = [x.strip() for x in os.popen("head -50 data.dat").readlines()]
curve, covid, sirps = [], [], []
fig, ax = None, None
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

if False:  # remember to revisit this again..embedding on the raw curves (would want to label with the other coords..)
    X = np.array([x for x in curve])
    print("fitting..")
    X_embedded = TSNE(n_components=2).fit_transform(X)

    print(X_embedded.shape)
    plt.plot(X_embedded)
    plt.tight_layout()
    plt.savefig("tsne_2d_curve.png")

if True:
    dx = [covid[i] + sirps[i] for i in range(len(covid))]
    X = np.array(dx)
    X = TSNE(n_components=3).fit_transform(X) # print(X.shape)
    n = X.shape[0]
    N = range(n)
    rgb = [covid[i] for i in N]
    r_min = min(np.array([covid[i][0] for i in N]))
    r_max = max(np.array([covid[i][0] for i in N]))
    g_min = min(np.array([covid[i][1] for i in N]))
    g_max = max(np.array([covid[i][1] for i in N]))
    b_min = min(np.array([covid[i][2] for i in N]))
    b_max = max(np.array([covid[i][2] for i in N]))
    rgb = [[(rgb[i][0] - r_min) / (r_max - r_min), 
            (rgb[i][1] - g_min) / (g_max - g_min), 
            (rgb[i][2] - b_min) / (b_max - b_min)] for i in N]

    if ANIMATION_MODE:
        fig = plt.figure(figsize=(16, 9), tight_layout=True, dpi=300)
    else:
        # https://matplotlib.org/stable/gallery/mplot3d/subplot3d.html
        # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax =[None, None]
        ax[0] = fig.add_subplot(1, 2, 1, projection='3d')
        ax[1] = fig.add_subplot(1, 2, 2)

        #fig, ax = plt.subplots(1, 2) # horizontal plots
    if ANIMATION_MODE:
        plt.rcParams['axes.facecolor'] = 'black'

    def on_pick(event):
        ax[1].clear()
        i = event.ind
        print("pick:", i)
        for x in i:
            print("covid", covid[x], "sirps", sirps[x]) # print("\t", curve[x])
            ax[1].plot(curve[x], label='HzR, sizF, mF, bta, gama, R0=' + ', '.join([str(round(q,4)) for q in (covid[x] + sirps[x])]))
        ax[1].legend()
        plt.draw()


    def init():
        global ax
        ax0 = ax if ANIMATION_MODE else ax[0]
        if ANIMATION_MODE:
            ax0 = plt.axes(projection='3d')
            ax0.set_facecolor('black')
        else:
            ax[1].plot(curve[0])
        ax0.scatter3D(X[:, 0], X[:, 1], X[:, 2], c=rgb, picker=True if INTERACTIVE_MODE else False) # cmap='Greens')

        if INTERACTIVE_MODE:
            fig.canvas.mpl_connect('pick_event', on_pick)

        return fig,
    
    TF = 11  # time scaling factor
    # rotate the axes and update
    # for angle in range(0, 360):
    n_frames = 360 * TF
    def animate(i):
        ax.set_title("tSNE 3d proj. of (HzR, sizeF, mF, beta, gamma, R0).." +
                     "r,g,b= (HzR, sizeF, mF)")  
        print("render " + str(i) + " / " + str(n_frames))
        j = i / TF
        ax.view_init(45 - j/(TF / 2.5), j) # angle)
        return fig,
        #plt.pause(.001)
    
    if ANIMATION_MODE:
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=n_frames, interval=0, blit=True)
        anim.save('tSNE_vid_' + str(TF) + '_.mp4', fps=60, extra_args=['-vcodec', 'libx264'])
    
    else:
        init()
        plt.tight_layout()
        plt.show()
        # plt.savefig("tnse_2d_params.png")


'''
def pick_scatter_plot():
    # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

    x, y, c, s = rand(4, 100)

    def onpick3(event):
        ind = event.ind
        print('onpick3 scatter:', ind, x[ind], y[ind])

    fig, ax = plt.subplots()
    ax.scatter(x, y, 100*s, c, picker=True)
    fig.canvas.mpl_connect('pick_event', onpick3)
'''


'''object picking..

https://matplotlib.org/stable/users/event_handling.html#object-picking

https://matplotlib.org/stable/gallery/event_handling/pick_event_demo.html '''
