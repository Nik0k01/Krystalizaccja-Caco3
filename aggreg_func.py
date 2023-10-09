import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d

def aggreg_func(sz_1, sz_2=30e-9, **kargs):
    """
    Ta funkcja ma za zadanie opisać w uproszczony sposób proces aglomeracji w reaktorze
    """
    # sz_1 - rozmiar, do którego krytształy aglomerują
    # sz_2 - rozmiar, od którego kryształy aglomerują - składowe aglomeratów
    # w kargs podawane są ilości kryształów o rozmiarze sz_1 i sz_2, które były w układzie w poprzednim kroku całkowania
    # Stała agregacji - Rigopulos
    k_a = 1.2
    # Stała wykładnicza wzrostu kryształu
    g = 2.0
    
    # Stopień przesycenia
    lambda_s = np.float64(kargs['lambda_s'])
    # Ilość kryształów o rozmiarze n_L - rozmiar do którego aglomerują dwa kryształy
    n_L = np.float64(kargs['n_L'])
    # Ilość kryształów o rozmiarze n_0
    n_0 = np.float64(kargs['n_0'])
    
    def beta_kernel(sz_1, sz_2):
        # Szybkość agregacji wg. równania 22
        return np.array(k_a * (lambda_s - 1) ** g * (sz_2 + sz_1))
    
    # Liniowa aproksymacja rozkładu liczbowego kryształu - potrzebna do numerycznej całki 
    f = interp1d(np.array([sz_2, sz_1]), np.array([n_0, n_L]), fill_value="extrapolate") # type: ignore
    
    def integrand(x, n_L=100) :
        # Liczba narodzin agregatów
        a = sz_1 / 2 * beta_kernel((sz_1**3 - x**3)**(1/3), x) * f(sz_1 - x) * f(x)
        # Liczba śmierci
        b = n_L * beta_kernel(sz_1, x) * f(x)
        return a - b
    
    c = integrate.quad(integrand, 0, sz_1, args=[n_L])
    return c[0]