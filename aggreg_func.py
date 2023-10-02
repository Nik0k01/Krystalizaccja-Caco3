import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d

def aggreg_func(sz_1, sz_2=30e-9, **kargs):
    """
    Ta funkcja ma za zadanie opisać w uproszczony sposób proces aglomeracji w reaktorze
    """
    
    k_a = 2.3
    g = 2.0
    lambda_s = np.float64(kargs['lambda_s'])
    n_L = np.float64(kargs['n_L'])
    n_0 = np.float64(kargs['n_0'])
    
    def beta_kernel(sz_1, sz_2):
        return np.array(k_a * (lambda_s - 1) ** g * (sz_2 + sz_1))
    
    f = interp1d(np.array([sz_2, sz_1]), np.array([n_0, n_L]), fill_value="extrapolate") # type: ignore
    
    def integrand(x, n_L=100) :
        a = sz_1 / 2 * beta_kernel((sz_1**3 - x**3)**(1/3), x) * f(sz_1 - x) * f(x)
        b = n_L * beta_kernel(sz_1, x) * f(x)
        return a - b
    c = integrate.quad(integrand, 0, sz_1, args=[n_L])
    return c[0]