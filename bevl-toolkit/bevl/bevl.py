from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Sequence, Dict
from scipy.optimize import brentq
from .gamma import dollar_gamma_bs
from .utils import brent_safe

@dataclass
class PathSet:
    S_paths: np.ndarray
    dt: float
    t_grid: np.ndarray
    N: int
    K: int

def build_paths_from_returns(S0: float, ret_windows: np.ndarray, dt: float) -> PathSet:
    N,K = ret_windows.shape
    S_paths = np.empty((N,K+1))
    S_paths[:,0]=S0
    rets = np.exp(ret_windows.copy())
    S_paths[:,1:] = S0 * np.cumprod(rets, axis=1)
    t_grid = dt * np.arange(1, K+1)
    return PathSet(S_paths=S_paths, dt=dt, t_grid=t_grid, N=N, K=K)

def _objective(sigma, pathset: PathSet, K_strike: float, r: float, q: float, weights: np.ndarray):
    S = pathset.S_paths
    logrets = np.log(S[:,1:]/S[:,:-1])
    rv = (logrets**2)/pathset.dt
    tau = (pathset.t_grid)[None,:]
    Snk = S[:,1:]
    DG = dollar_gamma_bs(Snk, K_strike, tau, r=r, q=q, sigma=sigma)
    kern = np.exp(-r*tau) * DG * pathset.dt
    diff = rv - sigma**2
    val_per_path = (kern*diff).sum(axis=1)
    return float((weights * val_per_path).sum())

def find_bevl_for_strike(pathset: PathSet, K_strike: float, r=0.0, q=0.0, weights=None, bracket=(1e-4,3.0)):
    if weights is None:
        weights = np.ones(pathset.N)/pathset.N
    f = lambda s: _objective(s, pathset, K_strike, r, q, weights)
    a,b = brent_safe(f, a=bracket[0], b=bracket[1])
    return brentq(f, a, b, maxiter=200, rtol=1e-6)

def bevl_surface(pathset: PathSet, strikes: Sequence[float], r=0.0, q=0.0, weights=None) -> Dict[float,float]:
    out = {}
    for K in strikes:
        out[float(K)] = find_bevl_for_strike(pathset, K, r=r, q=q, weights=weights)
    return out
