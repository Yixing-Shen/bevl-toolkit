from __future__ import annotations
import numpy as np, pandas as pd

def load_price_csv(path:str)->pd.DataFrame:
    df=pd.read_csv(path)
    df.columns=[c.lower() for c in df.columns]
    df['date']=pd.to_datetime(df['date'])
    df=df.sort_values('date').reset_index(drop=True)
    return df[['date','close']].dropna()

def make_windows_from_prices(df, tenor_steps:int):
    prices=df['close'].to_numpy(dtype=float)
    logprices=np.log(prices)
    logrets=np.diff(logprices)
    K=tenor_steps
    N=len(logrets)-K+1
    if N<=1: raise ValueError('Not enough data to form windows.')
    windows=np.lib.stride_tricks.sliding_window_view(logrets, K)  # (N,K)
    S0=float(prices[-1]); dt=1.0/252.0
    return windows.copy(), S0, dt
