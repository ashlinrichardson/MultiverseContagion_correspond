''' adapted from [1]'''
import numpy as np
import scipy
import matplotlib.pyplot as plt
import scipy.integrate
from scipy.optimize import minimize
odeint = scipy.integrate.odeint

'''Number of Days: fixed. To optimize:

initial S, initial E, initial I, initial R, beta, sigma, gamma'''
mean = None # ABM curve to fit to!
tspan = None

def read_lines(fn): # specific rendition of readlines()
    return [x.strip() for x in open(fn).read().strip().split('\n')]

def ode_model(z, # S, E, I, R: Susceptible, Exposed, Infectious, Recovered
              t, # time
              beta, # parameter that converts S into E
              sigma, # paramter that converts E into I
              gamma): # parameter that converts I into R
    """ Reference https://www.idmod.org/docs/hiv/model-seir.html"""
    S, E, I, R = z
    N = S + E + I + R
    dSdt = -beta*S*I/N
    dEdt = beta*S*I/N - sigma*E
    dIdt = sigma*E - gamma*I
    dRdt = gamma*I
    return [dSdt, dEdt, dIdt, dRdt]

def ode_solver(t, initial_conditions, params): # ODE solver
    initE, initI, initR, initN = initial_conditions
    beta, sigma, gamma = params
    initS = initN - (initE + initI + initR)
    res = odeint(ode_model, [initS, initE, initI, initR], t, args=(beta, sigma, gamma))
    return res


def curve(X):
    global tspan
    init_S, init_E, init_I, init_R, beta, sigma, gamma = X
    init_N = init_S + init_E + init_I + init_R

    initial_conditions = [init_E, init_I, init_R, init_N]
    params = [beta, sigma, gamma]
    # print("tspan", tspan)
    sol = ode_solver(tspan, initial_conditions, params)
    S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    return tspan, S, E, I, R

def my_residual(X):
    init_S, init_E, init_I, init_R, beta, sigma, gamma = X
    init_N = init_S + init_E + init_I + init_R

    t, S, E, I, R = curve(X)
    infections = init_N - S # contrived. Need to fix this!
    residual = [mean[i] - infections[i] for i in range(len(mean))]
    residual = np.sum(np.power(np.array(residual), 2.))
    return residual

def integrate(x, dt=1):
    result, i = [], 0
    for j in range(0, len(x)):
        i += (x[j] * dt)
        result.append(i)
    return result

def main(initN=1380000000, initE=1, initI=1, initR=.7, sigma=1/5.2, gamma=1/2.9, mu=0.034, R0=1.5, days=200):
    beta = R0 * gamma
    initial_conditions = [initE, initI, initR, initN]
    params = [beta, sigma, gamma]
    tspan = np.arange(0, days, 1)
    sol = ode_solver(tspan, initial_conditions, params)
    S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    t = tspan
    return [t, S, E, I, R]

def plots(X, fn):
    plt.figure()
    t, S, E, I, R = curve(X)
    plot_SEIR = False
    if plot_SEIR:
        plt.plot(t, S, label='Susceptible')
        plt.plot(t, E, label='Exposed')
        print("E", E)
        plt.plot(t, I, label='Infected')
        plt.plot(t, R, label='Recovered')
    
    # dt = t[1] - t[0]
    plt.plot(t, S[0] - S, label='Infections') # this is what we will correlate with ABM for now..
    plt.plot(t, mean, label='ABM mean')
    plt.legend()
    plt.savefig(fn) # "seir.png")

def init_abm(): # guess at initializing SEIR from Agent Based Model
    global mean
    global tspan
    init_N = 0
    lines = read_lines('param.csv') # get population guess from param.csv
    for line in lines:
        w = line.split(',')
        if w[0] == 'population':
            init_N = float(w[1])

    print("S=", init_N) # guess at S
    lines = read_lines('mean.csv') # get number of generations from abm mean file
    days = float(len(lines))
    mean = [float(x) for x in lines]

    init_E=1 # 1 # adjust these later?
    init_I=1 #1
    init_R=1 # .7
    sigma=1/5.2
    gamma=1/2.9
    mu=0.034
    R0=1.5
    beta = R0 * gamma
    init_S = init_N - init_E - init_I - init_R
    print("init_S", init_S)

    tspan = np.array(range(0, int(days)), dtype=float)
    X = [init_S, init_E, init_I, init_R, beta, sigma, gamma]
    print(X)
    a = curve(X)
    # print(a)

    xmin = X
    r = my_residual(X)


    plots(X, "seir1.png")


    for db in range(0, 300):
        init_S = 0.001 + float(db)/1000.
        X = [init_S, init_E, init_I, init_R, beta, sigma, gamma]
        R = my_residual(X)
        print(R)
        if R < r:
            xmin = X

    plots(xmin, "seir2.png")



    '''
    print("start")
    print("residual: ", my_residual(x_0))

    res = minimize(my_residual,
                   x_0,
                   method='SLSQP',
                   bounds=((0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None)),
                   options={'disp':True}) #                   options={'xatol': 1e-8, 'disp': True})

    print(res.x)
    '''
    
init_abm()

