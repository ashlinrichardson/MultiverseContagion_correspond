''' adapted from [1]'''
import numpy as np
import scipy
import matplotlib.pyplot as plt
import scipy.integrate
odeint = scipy.integrate.odeint

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

def integrate(x, dt=1):
    result, i = [], 0
    for j in range(0, len(x)):
        i += (x[j] * dt)
        result.append(i)
    return result

def main(initN=1380000000, initE=1, initI=1, initR=0, initD=0, sigma=1/5.2, gamma=1/2.9, mu=0.034, R0=4., days=200):
    beta = R0 * gamma
    initial_conditions = [initE, initI, initR, initN]
    params = [beta, sigma, gamma]
    tspan = np.arange(0, days, 1)
    sol = ode_solver(tspan, initial_conditions, params)
    S, E, I, R = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    t = tspan
    return [t, S, E, I, R]

def plots(initN, t, S, E, I, R, mean):
    plt.plot(t, S, label='Susceptible')
    plt.plot(t, E, label='Exposed')
    print("E", E)
    plt.plot(t, I, label='Infected')
    plt.plot(t, R, label='Recovered')
    dt = t[1] - t[0]
    plt.plot(t, initN - S, label='Infections') # this is what we will correlate with ABM for now..
    plt.plot(t, mean, label='ABM mean')
    plt.legend()
    plt.savefig("seir.png")

def init_abm(): # guess at initializing SEIR from Agent Based Model
    S = 0
    lines = read_lines('param.csv') # get population guess from param.csv
    for line in lines:
        w = line.split(',')
        if w[0] == 'population':
            S = float(w[1])

    print("S=", S) # guess at S
    lines = read_lines('mean.csv') # get number of generations from abm mean file
    days = float(len(lines))
    mean = [float(x) for x in lines]


    t, S, E, I, R = main(initN=S, days=days)
    plots(S, t, S, E, I, R, mean)
    

init_abm()

'''
interact(main,
         initE=IntSlider(min=0, max=100000, step=1, value=initE, description='initE', style=style, layout=slider_layout),
         initI=IntSlider(min=0, max=100000, step=10, value=initI, description='initI', style=style, layout=slider_layout),
         initR=IntSlider(min=0, max=100000, step=10, value=initR, description='initR', style=style, layout=slider_layout),
         initD=IntSlider(min=0, max=100000, step=10, value=initD, description='initD', style=style, layout=slider_layout),
         initN=IntSlider(min=0, max=1380000000, step=1000, value=initN, description='initN', style=style, layout=slider_layout),
         beta=FloatSlider(min=0, max=4, step=0.01, value=beta, description='Infection rate', style=style, layout=slider_layout),
         sigma=FloatSlider(min=0, max=4, step=0.01, value=sigma, description='Incubation rate', style=style, layout=slider_layout),
         gamma=FloatSlider(min=0, max=4, step=0.01, value=gamma, description='Recovery rate', style=style, layout=slider_layout),
         mu=FloatSlider(min=0, max=1, step=0.01, value=mu, description='Mortality rate', style=style, layout=slider_layout),
         days=IntSlider(min=1, max=600, step=7, value=days, description='Days', style=style, layout=slider_layout)
        );

references:
[1] https://towardsdatascience.com/simulating-compartmental-models-in-epidemiology-using-python-jupyter-widgets-8d76bdaff5c2
[2] https://towardsdatascience.com/infectious-disease-modelling-beyond-the-basic-sir-model-216369c584c4
[3] https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model
[4] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7277829/

'''
