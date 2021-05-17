# https://stackoverflow.com/questions/34422410/fitting-sir-model-based-on-least-squares # based on
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize

def err(m):
    print("Error: " + m); sys.exit(1)

def read_lines(f):
    lines = [x.strip() for x in open(f).read().strip().split('\n')]
    return lines

population = float(int(open('sir.csv.pop_size').read())) # read population size
infected = float(int(open('sir.csv.infected').read())) # read number of initial infections

ydata = [x.strip() for x in open("mean.csv").readlines()] # from plot_density.py
xdata = [float(x) for x in range(len(ydata))]

ydata = np.array(ydata, dtype=float)  # convert to np float array format
xdata = np.array(xdata, dtype=float)

ydata += infected # add on the number of initial infections to get number of non-susceptible
plt.plot(xdata, ydata)
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

def fit_agentbased():
    pass

sys.exit(1)

N = population # 500 # need to read this from param.csv!!!
I0 = ydata[0] # initial infections: take this to be the first observation. Natural assumption!
S0 = N - I0 # subtract the non-susceptible from the population size to get susceptible. Rocket science!
R0 = 0.0 # lower bound? this should grow from there..

popt, pcov = optimize.curve_fit(fit_odeint, xdata, ydata)
fitted = fit_odeint(xdata, *popt)

beta, gamma = popt
R0 = beta / gamma 
print("beta", beta, "gamma", gamma, "R0", R0)

plt.plot(xdata, ydata, '+', label="data", color='b')
plt.plot(xdata, fitted, label="SIR model", color='r')
plt.title("SIR model fit to CovidSIM console.log")
plt.xlabel('step')
plt.ylabel('number of non-susceptible')
plt.legend()
plt.show()

print('+w sir.csv')
f = open('sir.csv', 'wb')
f.write(('\n'.join([str(x) for x in fitted.tolist()])).encode())
f.close()

print('+w sir.csv.pop_size')
open('sir.csv.pop_size', 'wb').write(str(int(population)).encode())

