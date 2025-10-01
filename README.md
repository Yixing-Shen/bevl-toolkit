# BEVL Toolkit: Break-Even Volatility Surface Construction

## 📖 Introduction
**BEVL (Break-Even Volatility)** is the volatility that makes the **expected P&L of a delta-hedged option equal to zero** (Dupire, 2006).  
Unlike market-implied volatility, BEVL is computed by averaging realized variances **weighted by option Gamma** along different paths.

This repository provides a minimal but extendable **Python toolkit** to:
- Construct BEVL surfaces from historical return paths
- Apply different weighting schemes (equal weights, realized-volatility similarity, KL-implied weights)
- Compare BEVL “virtual surfaces” against market implied volatility

---

## ⚙️ Features
- **Historical Path Simulation**: slice historical returns into windows matching target tenors and rebase to today’s spot.  
- **Gamma Weighting**: compute Black–Scholes dollar Gamma for each path, strike, and time step.  
- **Weighting Schemes**:  
  - Equal weights  
  - Realized-vol similarity weights (Gaussian kernel)  
  - KL-implied weights (weighted Monte Carlo calibration to market IVs)  
- **Surface Construction**: Brent root-finding for each strike → BEVL surface.  
- **Examples Included**: synthetic GBM demo + SPX sample data.

---
