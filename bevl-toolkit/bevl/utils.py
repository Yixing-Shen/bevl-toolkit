from __future__ import annotations
import numpy as np

def realized_var_from_logrets(logrets: np.ndarray, dt: float) -> np.ndarray:
    return (logrets**2) / dt

def brent_safe(f, a=1e-4, b=3.0, max_expand=6):
    fa = f(a); fb = f(b); s=0
    while fa*fb>0 and s<max_expand:
        b*=2.0; fb=f(b); s+=1
    return a,b
