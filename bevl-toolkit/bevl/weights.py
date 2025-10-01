from __future__ import annotations
import numpy as np
from scipy.optimize import minimize

def equal_weights(N:int)->np.ndarray:
    w = np.ones(N); w/=w.sum(); return w

def realized_vol_similarity_weights(ret_windows: np.ndarray, recent: np.ndarray|None=None, h: float=0.1)->np.ndarray:
    N,K = ret_windows.shape
    if recent is None: recent = ret_windows[-1]
    rv_recent = (recent**2).mean()
    rv_paths = (ret_windows**2).mean(axis=1)
    d = rv_paths - rv_recent
    w = np.exp(-0.5*(d/(h+1e-12))**2)
    if not np.isfinite(w).all() or w.sum()==0: w=np.ones_like(w)
    return w / w.sum()

def implied_historical_weights(g_matrix: np.ndarray, prior: np.ndarray|None=None)->np.ndarray:
    M,N = g_matrix.shape
    if prior is None: prior = np.ones(N)/N
    prior = prior/prior.sum()

    def obj(p):
        eps=1e-12
        return float(np.sum(p*np.log((p+eps)/(prior+eps))))

    cons=[{'type':'eq','fun':lambda p: p.sum()-1.0}]
    for m in range(M):
        cons.append({'type':'eq','fun':lambda p, m=m: float(g_matrix[m].dot(p))})
    bnds=[(0.0,1.0)]*N
    x0=prior.copy()
    res=minimize(obj,x0,method='SLSQP',bounds=bnds,constraints=cons,options={'maxiter':1000,'ftol':1e-9})
    if not res.success:
        return prior
    p=res.x
    p=np.clip(p,0,1)
    s=p.sum()
    return p/s if s>0 else prior
