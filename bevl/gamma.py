from __future__ import annotations
import numpy as np
from scipy.stats import norm
import numpy as _np

def dollar_gamma_bs(S, K, tau, r=0.0, q=0.0, sigma=0.2):
    tau = _np.maximum(tau, 1e-8)
    S = _np.asarray(S, dtype=float)
    K = float(K)
    d1 = (_np.log(S/K) + (r - q + 0.5*sigma*sigma)*tau) / (sigma*_np.sqrt(tau))
    pdf = _np.exp(-0.5*d1*d1)/_np.sqrt(2.0*_np.pi)
    return S * pdf * _np.exp(-q*tau) / (sigma*_np.sqrt(tau))
