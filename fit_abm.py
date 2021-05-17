# https://stackoverflow.com/questions/34422410/fitting-sir-model-based-on-least-squares # based on

N_SIM = 1024 # number of simulations per point

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize

def err(m):
    print("Error: " + m); sys.exit(1)

def run(c):
    print('[' + c + ']')
    a = os.system(c + ' >>log.dat 2>&1')


def read_lines(f):
    lines = [x.strip() for x in open(f).read().strip().split('\n')]
    ret = []
    for line in lines:
        if line != '':
            ret.append(line)
    return ret

population = float(int(open('sir.csv.pop_size').read())) # read population size
infected = float(int(open('sir.csv.infected').read())) # read number of initial infections

ydata = [x.strip() for x in open("sir.csv").readlines()] # from plot_density.py
xdata = [float(x) for x in range(len(ydata))]

ydata = np.array(ydata, dtype=float)  # convert to np float array format
ydata -= infected # subtract number of initial infections from non-susceptible to get infections per step

def fix_array(my_data):
    print("\tfix data of len: " + str(len(my_data)) + " to len: " + str(len(xdata)))
    last = my_data[-1]
    # print(len(my_data), len(xdata))
    while len(my_data) < len(xdata): # if the abm stops early, assume the non-susceptibles at this point are fixed
        my_data.append(last)

    if len(my_data) > len(xdata):
        my_data = my_data[0: len(xdata)]
    return my_data

abm_mean = None
try:
    abm_mean = [float(x) for x in read_lines('mean.csv')]
    abm_mean = fix_array(abm_mean)
    print(abm_mean)
    abm_mean = np.array(abm_mean, dtype=float)
except:
    abm_mean = None

xdata = np.array(xdata, dtype=float)

pre_plot = False
if pre_plot:
    if abm_mean is not None:
        plt.plot(abm_mean, label='abm mean')
    plt.plot(ydata, label='sir model')
    plt.legend()
    plt.show()

'''

def sir_model(y, x, beta, gamma):
    S = -beta * y[0] * y[1] / N
    R = gamma * y[1]
    I = -(S + R)
    return S, I, R

def fit_odeint(x, beta, gamma):
    return N - integrate.odeint(sir_model, (S0, I0, R0), x, args=(beta, gamma))[:,0] # fit on nonsusceptible

'''

# Error: python3 write_csv [population size] [HzR] [sizeF] [mF] [RedDays] [N_infect] [N_simulation] # write tickets going no-where for single universe

def fit_agent(x, HzR, sizeF, mF):
    run('rm mean.csv *.txt *.grep') # for sanity..
    run(' '.join(['python3', 'write_csv_run.py', str(int(population)), str(HzR), str(sizeF), str(mF), 'None', str(int(infected)), str(N_SIM)]))
    run('python3 plot_density.py')
    mean = [float(x) for x in read_lines('mean.csv')]
    mean = fix_array(mean)
    mean = np.array(mean)
    # print("mean", mean)
    # mean -= infected
    return mean

popt, pcov = optimize.curve_fit(fit_agent, xdata, ydata, p0 = [.85, 1.5, .75])
fitted = fit_agent(xdata, *popt)
print(*popt)

HzR, sizeF, mF = popt
print('HzR', HzR, 'sizeF', sizeF, 'mF', mF)

plt.plot(xdata, ydata, '+', label="input data", color='b')
plt.plot(xdata, fitted, label="CovidSIM mean", color='r')
plt.title("CovidSIM mean fitted to input data")
plt.xlabel('step')
plt.ylabel('number of non-susceptible')
plt.legend()
plt.show()
