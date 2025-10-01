import argparse, os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from bevl import load_price_csv, make_windows_from_prices, build_paths_from_returns, bevl_surface
from bevl import equal_weights, realized_vol_similarity_weights, implied_historical_weights

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--csv', default=None, help='CSV with date,close. If None, generates synthetic GBM.')
    ap.add_argument('--tenor_days', type=int, default=21)
    ap.add_argument('--strikes', type=float, nargs='+', default=[0.9,0.95,1.0,1.05,1.1])
    ap.add_argument('--r', type=float, default=0.0); ap.add_argument('--q', type=float, default=0.0)
    ap.add_argument('--market_iv', type=float, nargs='*', default=[])
    args=ap.parse_args()

    if args.csv is None:
        np.random.seed(0); n=252*4; s0=4000.0; mu=0.05; vol=0.2; dt=1/252
        shocks=np.random.normal((mu-0.5*vol*vol)*dt, vol*np.sqrt(dt), n)
        prices=s0*np.exp(np.cumsum(shocks))
        dates=pd.date_range('2020-01-01', periods=n, freq='B')
        df=pd.DataFrame({'date':dates,'close':prices})
    else:
        df=load_price_csv(args.csv)

    windows, S0, dt = make_windows_from_prices(df, args.tenor_days)
    pathset = build_paths_from_returns(S0, windows, dt)
    strikes_abs=[S0*x for x in args.strikes]

    # equal & similarity
    w_eq = equal_weights(pathset.N)
    w_sim = realized_vol_similarity_weights(windows)
    surf_eq = bevl_surface(pathset, strikes_abs, r=args.r, q=args.q, weights=w_eq)
    surf_sim= bevl_surface(pathset, strikes_abs, r=args.r, q=args.q, weights=w_sim)

    results={'strike':args.strikes,'K_abs':strikes_abs,
             'BEV_equal':[surf_eq[k] for k in strikes_abs],
             'BEV_similarity':[surf_sim[k] for k in strikes_abs]}

    # optional: KL implied weights using given ATM IVs (simple demo)
    if len(args.market_iv)>0:
        # build g-matrix (M instruments x N paths)
        M=len(args.market_iv); N=pathset.N
        S=pathset.S_paths; rv=(np.log(S[:,1:]/S[:,:-1])**2)/pathset.dt
        tau=(pathset.t_grid)[None,:]; Snk=S[:,1:]
        from bevl.gamma import dollar_gamma_bs
        import numpy as np
        G=np.zeros((M,N))
        K_list=[S0]*M
        for m, (K, sig) in enumerate(zip(K_list, args.market_iv)):
            DG=dollar_gamma_bs(Snk, K, tau, r=args.r, q=args.q, sigma=sig)
            kern=np.exp(-args.r*tau)*DG*pathset.dt
            G[m,:]=(kern*(rv - sig**2)).sum(axis=1)
        from bevl.weights import implied_historical_weights
        w_imp=implied_historical_weights(G, prior=w_eq)
        surf_imp=bevl_surface(pathset, strikes_abs, r=args.r, q=args.q, weights=w_imp)
        results['BEV_implied']=[surf_imp[k] for k in strikes_abs]

    os.makedirs('outputs', exist_ok=True)
    out=pd.DataFrame(results); out.to_csv('outputs/bevl_surface.csv', index=False)
    print(out)

    plt.figure()
    plt.plot(results['strike'], results['BEV_equal'], label='Equal')
    plt.plot(results['strike'], results['BEV_similarity'], label='Similarity')
    if 'BEV_implied' in results: plt.plot(results['strike'], results['BEV_implied'], label='Implied (KL)')
    plt.xlabel('Moneyness (K/S0)'); plt.ylabel('BEV sigma'); plt.legend(); plt.title('BEVL Surface')
    plt.savefig('outputs/bevl_surface.png', dpi=150, bbox_inches='tight')

if __name__=='__main__':
    main()
