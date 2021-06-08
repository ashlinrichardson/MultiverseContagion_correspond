import os
import sys
import numpy as np
import matplotlib.pyplot as plt
def err(m):
    print("Error: " + m); sys.exit(1)

ms = [x.strip() for x in os.popen("ls -1 mean*csv").readlines()]
ms_n ={m.split('.')[0].split('_')[1] : m for m in ms}

ms_n = [[int(m), ms_n[m]] for m in ms_n]
ms_n.sort(reverse=False)
print(ms_n)

sd = [x.strip() for x in os.popen("ls -1 stdv*csv").readlines()]
sd_n = {m.split('.')[0].split('_')[1]: m for m in sd}
sd_n = [[int(m), sd_n[m]] for m in sd_n]
sd_n.sort(reverse=False)
print(sd_n)

if len(ms_n) != len(sd_n):
    err("1")

for i in range(0, len(ms_n)):
    if ms_n[i][0] != sd_n[i][0]:
        err("2")

m_f = [ms_n[i][1] for i in range(len(ms_n))]
s_f = [sd_n[i][1] for i in range(len(sd_n))]
j = [sd_n[i][0] for i in range(len(sd_n))]

max_T = 0
for i in range(len(m_f)):
    L = len(open(m_f[i]).readlines())
    if L > max_T:
        max_T = L

print("max_T", max_T)

fig_n = 0
for k in range(0, len(m_f)):
    plt.figure()
    for i in range(k + 1):
        m = [float(x) for x in open(m_f[i]).read().strip().split('\n')]
        s = [float(x) for x in open(s_f[i]).read().strip().split('\n')]

        X = m[-1]
        while len(m) < max_T:
            m += [X]

        X = s[-1]
        while len(s) < max_T:
            s += [X]

        plt.plot(m, label='n_sims=' + str(j[i]))
        plt.ylim([0, 45])
        plt.legend(loc="upper left")

    plt.title("Curves N = 100, initial_infect = 5")
    plt.xlabel("generation")
    plt.ylabel("|N - susceptible|")
    pfn = "plot_" + ('%02d' % fig_n) + '.png'
    plt.savefig(pfn)
    print("+w " + pfn)
    plt.close()
    fig_n += 1


for k in range(1, len(m_f)):
    plt.figure()
    for i in range(k):
        m = [float(x) for x in open(m_f[i + 1]).read().strip().split('\n')]

        X = m[-1]
        while len(m) < max_T:
            m += [X]

        m0 = [float(x) for x in open(m_f[i]).read().strip().split('\n')]

        X = m0[-1]
        while len(m0) < max_T:
            m0 += [X]

        print("i+1", i+1, "i", i)
        plt.plot((np.abs(np.array(m) - np.array(m0))), label='n_sims=' + str(j[i+1]) + ' vs ' + str(j[i]))
        plt.ylim([0, 7])
        plt.legend(loc="upper left")

    plt.title("Gap between successive curves. N = 100, initial_infect = 5")
    plt.xlabel("generation")
    plt.ylabel("||N - susceptible|_t - |N- susceptible|_(t-1)||")
    pfn = "plot_" + ('%02d' % fig_n) + '.png'
    plt.savefig(pfn)
    print("+w " + pfn)
    plt.close()
    fig_n += 1
