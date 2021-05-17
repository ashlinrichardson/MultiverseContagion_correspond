# https://stackoverflow.com/questions/34422410/fitting-sir-model-based-on-least-squares # based on

N_SIM = 64 # number of simulations per point

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
    a = os.system(c)


def read_lines(f):
    lines = [x.strip() for x in open(f).read().strip().split('\n')]
    return lines

population = float(int(open('sir.csv.pop_size').read())) # read population size
infected = float(int(open('sir.csv.infected').read())) # read number of initial infections

ydata = [x.strip() for x in open("sir.csv").readlines()] # from plot_density.py
xdata = [float(x) for x in range(len(ydata))]

ydata = np.array(ydata, dtype=float)  # convert to np float array format
ydata -= infected # subtract number of initial infections from non-susceptible to get infections per step

def fix_array(my_data):
    print("fix data of len: " + str(len(my_data)) + " to len: " + str(len(xdata)))
    global xdata
    last = my_data[-1]
    print(len(my_data), len(xdata))
    while len(my_data) < len(xdata): # if the abm stops early, assume the non-susceptibles at this point are fixed
        my_data.append(last)

    if len(my_data) > len(xdata):
        my_data = my_data[0: len(xdata)]
    return my_data

abm_mean = None
try:
    abm_mean = [float(x) for x in read_lines('mean.csv')]
    '''
    last = abm_mean[-1]
    print(len(abm_mean), len(xdata))
    while len(abm_mean) < len(xdata): # if the abm stops early, assume the non-susceptibles at this point are fixed
        abm_mean.append(last)

    if len(abm_mean) > len(xdata):
        abm_mean = abm_mean[0: len(xdata)]
    # only need to vis on same domain
    #
    '''
    abm_mean = fix_array(abm_mean)
    print(abm_mean)
    abm_mean = np.array(abm_mean, dtype=float)
except:
    abm_mean = None

xdata = np.array(xdata, dtype=float)
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
    mean = np.array([float(x) for x in read_lines('mean.csv')])
    print("mean", mean)
    # mean -= infected
    return mean

# fit_agentbased(xdata, 1, 1, 1)
# print("ydata", ydata)
# sys.exit(1)
# N = population # 500 # need to read this from param.csv!!!
# I0 = ydata[0] # initial infections: take this to be the first observation. Natural assumption!
# S0 = N - I0 # subtract the non-susceptible from the population size to get susceptible. Rocket science!
# R0 = 0.0 # lower bound? this should grow from there..

popt, pcov = optimize.curve_fit(fit_agent, xdata, ydata, p0 = [1., 1., 1.])
fitted = fit_odeint(xdata, *popt)
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

'''
print('+w sir.csv')
f = open('sir.csv', 'wb')
f.write(('\n'.join([str(x) for x in fitted.tolist()])).encode())
f.close()

print('+w sir.csv.pop_size')
open('sir.csv.pop_size', 'wb').write(str(int(population)).encode())
'''
