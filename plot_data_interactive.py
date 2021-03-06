'''this one should be run after write_csv_run_grid.py
.. should have a switch between video and interactive mode!'''
INTERACTIVE_MODE = True
RGB_COVIDSIM = True # False # True # False: rgb coloring from SIR coeff instead of covidsim coeff..
ANIMATION_MODE = not INTERACTIVE_MODE # disable user input to plot a video!
import os
import sys
import math
import pickle
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib import animation
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import RadioButtons

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 7}
mp.rc('font', **font)
COLOR = 'white' if ANIMATION_MODE else 'black'
mp.rcParams['text.color'] = COLOR
mp.rcParams['axes.labelcolor'] = COLOR
mp.rcParams['xtick.color'] = COLOR
mp.rcParams['ytick.color'] = COLOR

lines = [x.strip() for x in open("data.dat").readlines()]
# lines = [x.strip() for x in os.popen("head -50 data.dat").readlines()]  # low data volume for testing
curve, covid, sirps, curve_sir = [], [], [], []
n_covid, n_sir, rgb = None, None, None
fig, ax = None, None

def hscale(x):
    xx = x.tolist()
    xx.sort()
    p1 = int(math.floor(0.01 * len(xx)))
    bot, top = xx[p1], xx[-p1]
    f = 1. / (top - bot)
    xx = f * (x - bot)
    xx = xx.tolist()
    for i in range(len(xx)):
        if xx[i] < 0.:
            xx[i] = 0.
        if xx[i] > 1.:
            xx[i] = 1.
    return np.array(xx)

def set_rgb(use):
    global rgb
    n = X.shape[0]
    N = range(n)
    rgb = [use[i] for i in N]
    reds = np.array([use[i][0] for i in N])
    blus = np.array([use[i][1] for i in N])
    grns = np.array([use[i][2] for i in N])
    reds.sort()
    blus.sort()
    grns.sort()

    p2i = int(.5 + math.floor(0.01 * len(N)))
    r_min = reds[p2i]
    r_max = reds[len(N) - p2i - 1]
    b_min = blus[p2i]
    b_max = blus[len(N) - p2i - 1]
    g_min = grns[p2i]
    g_max = grns[len(N) - p2i - 1]
    print("rmin", r_min, "rmax", r_max)
    print("gmin", g_min, "gmax", g_max)
    print("bmin", b_min, "bmax", b_max)
    rgb = [[max(0., min(1., (rgb[i][0] - r_min) / (r_max - r_min))), 
            max(0., min(1., (rgb[i][1] - g_min) / (g_max - g_min))), 
            max(0., min(1., (rgb[i][2] - b_min) / (b_max - b_min)))] for i in N]


def init(my_par=None):
    global rgb
    print("init..", my_par)
    xx, yy, zz = X[:, 0], X[:, 1], X[:,2]
    xL, yL, zL = 'tsneX', 'tsneY', 'tsneZ'
    n = X.shape[0]
    N = range(n)

    if my_par == 'x_covid':
        xx = np.array([c[0] for c in covid])
        yy = np.array([c[1] for c in covid])
        zz = np.array([c[2] for c in covid])
        xL, yL, zL = 'HzR', 'sizeF', 'mF' 
        set_rgb(sirps)

    if my_par == 'x_sir':
        xx = np.array([c[0] for c in sirps])
        yy = np.array([c[1] for c in sirps])
        zz = np.array([c[2] for c in sirps])
        xx = hscale(xx)
        yy = hscale(yy)
        zz = hscale(zz)
        xL, yL, zL = 'beta', 'gamma', 'R0'
        set_rgb(covid)

    global ax
    ax0 = ax if ANIMATION_MODE else ax[0]
    ax0.clear()
    if ANIMATION_MODE:
        ax0 = plt.axes(projection='3d')
        ax0.set_facecolor('black')
    else:
        ax[1].plot(curve[0])
    ax0.scatter3D(xx, yy, zz, c=rgb, picker=True if INTERACTIVE_MODE else False)
    ax0.set_xlabel(xL)
    ax0.set_ylabel(yL)
    ax0.set_zlabel(zL)
    if INTERACTIVE_MODE:
        fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()
    return fig,

ci = 0
for line in lines:
    ci += 1
    if ci ==1:
        continue
    w = line.split(",")

    # print("ci", ci, w)
    csi = [float(x) for x in w[0:3]]
    sir = [float(x) for x in w[3:6]]

    n_covid = int(w[6])
    n_sir   = int(w[7])

    cur = [float(x) for x in w[8: 8 + n_covid]]
    cur_sir = [float(x) for x in w[8 + n_covid: 8 + n_covid + n_sir]]

    curve.append(cur)
    covid.append(csi)
    sirps.append(sir)
    curve_sir.append(cur_sir)
# print("covid", covid)
# print("sirps", sirps)

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
    # dx = [curve[i] + curve_sir[i] for i in range(len(covid))]
    X = np.array(dx)
    if not os.path.exists('tsne.dat'):
        X = TSNE(n_components=3, verbose=True).fit_transform(X) # print(X.shape)
        print("save tSNE..")
        pickle.dump(X, open('tsne.dat', 'wb'))
    else:
        print("reload tSNE..")
        X = pickle.load(open('tsne.dat', 'rb')) 
    n = X.shape[0]
    N = range(n)
    use = covid if RGB_COVIDSIM else sirps
    rgb = [use[i] for i in N]
    reds = np.array([use[i][0] for i in N])
    blus = np.array([use[i][1] for i in N])
    grns = np.array([use[i][2] for i in N])
    reds.sort()
    blus.sort()
    grns.sort()

    p2i = int(.5 + math.floor(0.005 * len(N)))

    r_min = reds[p2i]
    r_max = reds[len(N) - p2i - 1]
    b_min = blus[p2i]
    b_max = blus[len(N) - p2i - 1]
    g_min = grns[p2i]
    g_max = grns[len(N) - p2i - 1]
    # r_min = min(np.array([use[i][0] for i in N]))
    # r_max = max(np.array([use[i][0] for i in N]))
    # g_min = min(np.array([use[i][1] for i in N]))
    # g_max = max(np.array([use[i][1] for i in N]))
    # b_min = min(np.array([use[i][2] for i in N]))
    # b_max = max(np.array([use[i][2] for i in N]))
    print("rmin", r_min, "rmax", r_max)
    print("gmin", g_min, "gmax", g_max)
    print("bmin", b_min, "bmax", b_max)

    rgb = [[max(0., min(1., (rgb[i][0] - r_min) / (r_max - r_min))), 
            max(0., min(1., (rgb[i][1] - g_min) / (g_max - g_min))), 
            max(0., min(1., (rgb[i][2] - b_min) / (b_max - b_min)))] for i in N]

    if ANIMATION_MODE:
        fig = plt.figure(figsize=(16, 9), tight_layout=True, dpi=300)
    else:
        # https://matplotlib.org/stable/gallery/mplot3d/subplot3d.html
        # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
        # fig = plt.figure(figsize=plt.figaspect(0.5))
        fig, axs = plt.subplots(1,3,gridspec_kw={'width_ratios': [3, 1.5, .5]})
        ax =[axs[0], axs[1]]
        ax[0] = fig.add_subplot(1, 3, 1, projection='3d')
        ax[1] = fig.add_subplot(1, 3, 2)
        axs[2] = fig.add_subplot(1,3,3) # , gridspec_kw={'width_ratios': [3, 3, 1]})
        radio = RadioButtons(axs[2], ('x_tsne', 'x_covid', 'x_sir'))
        radio.on_clicked(init)
        plt.tight_layout()
        #fig, ax = plt.subplots(1, 2) # horizontal plots
    if ANIMATION_MODE:
        plt.rcParams['axes.facecolor'] = 'black'

    '''object picking..
    https://matplotlib.org/stable/users/event_handling.html#object-picking
    https://matplotlib.org/stable/gallery/event_handling/pick_event_demo.html '''
    def on_pick(event):
        ax[1].clear()
        i = event.ind
        print("pick:", i)
        ci = 0
        for x in i:
            print("covid", covid[x], "sirps", sirps[x]) # print("\t", curve[x])
            var = ['HzR', 'sizF', 'mF', 'bta', 'gama', 'R0']
            dta = [str(round(q,4)) for q in (covid[x] + sirps[x])]
            print("curve", curve[x])
            cols = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
            ax[1].plot(curve[x], label=' '.join([var[q] + '=' + dta[q] for q in range(len(var))]), color=cols[ci]) #     + ', '.join())
            ax[1].plot(curve_sir[x], label=' '.join([var[q] + '=' + dta[q] for q in range(len(var))]) + "(sir fit)", color=cols[ci], linestyle='--')
            ci += 1
        ax[1].legend()
        ax[1].set_ylim([0, 500])
        plt.draw()



    
    my_init = init 

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
