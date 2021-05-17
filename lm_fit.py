import numpy as np
import lmfit
import matplotlib.pyplot as plt
from lmfit.lineshapes import gaussian, lorentzian
np.random.seed(42)
x = np.linspace(0, 20.0, 1001)

data = (gaussian(x, 21, 6.1, 1.2) + np.random.normal(scale=0.1, size=x.size))  # normal distr. with some noise
plt.plot(x, data);

def f(x, a, b, c):
    return gaussian(x, a, b, c)

mod = lmfit.Model(f)
# we set the parameters (and some initial parameter guesses)
mod.set_param_hint("a", value=10.0, vary=True)
mod.set_param_hint("b", value=10.0, vary=True)
mod.set_param_hint("c", value=10.0, vary=True)

params = mod.make_params()

result = mod.fit(data, params, method="leastsq", x=x)  # fitting
plt.figure(figsize=(8,4))
result.plot_fit(datafmt="-");
result.best_values

plt.show()