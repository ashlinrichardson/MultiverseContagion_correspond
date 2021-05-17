# need to read params from param.csv!!!!!
# https://stackoverflow.com/questions/34422410/fitting-sir-model-based-on-least-squares
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize

def err(m):
    print("Error: " + m); sys.exit(1)

def read_lines(f):
    lines = [x.strip() for x in open(f).read().strip().split('\n')]
    return lines

lines = read_lines('param.csv')  # read the parameter file to get the population size!
w = lines[1].strip(',').split(',')
if w[0] != 'population':
    err('expected: population: found: ' + w[0])
population = float(int(w[1]))
print("population", population)

w = lines[7].strip(',').split(',')  # read the pop file name from param.csv
if w[0] != 'pop file':
    err('expected: pop file')
pop_file = w[1]
print("pop_file", pop_file)

w = lines[8].strip(',').split(',') # read the case file name from param.csv
if w[0] != 'case file':
    err('expected: case file')
case_file = w[1]
print("case_file", case_file)

c = {} # pragmatic programming: find unique pID for initial cases
lines = json.loads(open(case_file).read())['x']  # read case file data
for line in lines:
    w = line.strip().split(',')
    try:
        x = int(w[0])
        if x not in c: c[x] = 0
        c[x] += 1
    except:
        pass
infected = float(len(c.keys()))  # count the number of initial infections

'''
ydata = ['1e-06', '1.49920166169172e-06', '2.24595472686361e-06', '3.36377954575331e-06', '5.03793663882291e-06', '7.54533628058909e-06', '1.13006564683911e-05', '1.69249500601052e-05', '2.53483161761933e-05', '3.79636391699325e-05', '5.68567547875179e-05', '8.51509649182741e-05', '0.000127522555808945', '0.000189928392105942', '0.000283447055673738', '0.000423064043409294', '0.000631295993246634', '0.000941024110897193', '0.00140281896645859', '0.00209085569326554', '0.00311449589149717', '0.00463557784224762', '0.00689146863803467', '0.010227347567051', '0.0151380084180746', '0.0223233100045688', '0.0327384810150231', '0.0476330618585758', '0.0685260046667727', '0.0970432959143974', '0.134525888779423', '0.181363340075877', '0.236189247803334', '0.295374180276257', '0.353377036130714', '0.404138746080267', '0.442876028839178', '0.467273954573897', '0.477529937494976', '0.475582401936257', '0.464137179474659', '0.445930281787152', '0.423331710456602', '0.39821360956389', '0.371967226561944', '0.345577884704341', '0.319716449520481', '0.294819942458255', '0.271156813453547', '0.24887641905719', '0.228045466022105', '0.208674420183194', '0.190736203926912', '0.174179448652951', '0.158937806544529', '0.144936441326754', '0.132096533873646', '0.120338367115739', '0.10958340819268', '0.099755679236243', '0.0907826241267504', '0.0825956203546979', '0.0751302384111894', '0.0683263295744258', '0.0621279977639921', '0.0564834809370572', '0.0513449852139111', '0.0466684871328814', '0.042413516167789', '0.0385429293775096', '0.035022685071934', '0.0318216204865132', '0.0289112368382048', '0.0262654939162707', '0.0238606155312519', '0.021674906523588', '0.0196885815912485', '0.0178836058829335', '0.0162435470852779', '0.0147534385851646', '0.0133996531928511', '0.0121697868544064', '0.0110525517526551', '0.0100376781867076', '0.00911582462544914', '0.00827849534575178', '0.00751796508841916', '0.00682721019158058', '0.00619984569061827', '0.00563006790443123', '0.00511260205894446', '0.00464265452957236', '0.00421586931435123', '0.00382828837833139', '0.00347631553734708', '0.00315668357532714', '0.00286642431380459', '0.00260284137520731', '0.00236348540287827', '0.00214613152062159', '0.00194875883295343']
xdata = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101']
'''

ydata = [x.strip() for x in open("mean.csv").readlines()] # from plot_density.py
xdata = [float(x) for x in range(len(ydata))]

ydata = np.array(ydata, dtype=float)  # convert to np float array format
xdata = np.array(xdata, dtype=float)

ydata += infected # ydata will refer to the number of nonsusceptible.. after adding on the initial infections

def sir_model(y, x, beta, gamma):
    S = -beta * y[0] * y[1] / N
    R = gamma * y[1]
    I = -(S + R)
    return S, I, R

def fit_odeint(x, beta, gamma):
    return N - integrate.odeint(sir_model, (S0, I0, R0), x, args=(beta, gamma))[:,0] # fit on nonsusceptible

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
