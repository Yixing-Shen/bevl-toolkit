# Methodology: Break-Even Volatility (BEVL)

## 1. Concept

Break-Even Volatility (BEVL) is defined as the volatility that makes the **expected P&L of a delta-hedged option equal to zero**.  

For a European option priced under Black–Scholes dynamics with volatility parameter \(\sigma\), if we delta-hedge along a realized path \(\{S_t\}\), the discrete hedging error is:

\[
d\Pi_t = \frac{1}{2} \, \Gamma^{BS}(t, S_t; \sigma) \, S_t^2 \, \big( \sigma_t^2 - \sigma^2 \big) \, dt
\]

where:
- \(\Gamma^{BS}(t, S_t; \sigma)\): Black–Scholes Gamma under volatility \(\sigma\)  
- \(\sigma_t^2\): realized instantaneous variance along the path  

BEVL \(\sigma_{BE}\) is the volatility such that:

\[
\mathbb{E}\!\left[ \int_0^T e^{-rt} \, S_t^2 \, \Gamma^{BS}(t, S_t; \sigma_{BE}) \, \big(\sigma_t^2 - \sigma_{BE}^2\big) dt \right] = 0
\]

---

## 2. Discretization

Given \(N\) simulated or historical paths (indexed by \(n\)) and discrete time steps (indexed by \(k\)):

\[
\sum_{n=1}^N p_n \sum_{k=1}^K e^{-rt_k} \, S_{n,k}^2 \, \Gamma^{BS}(t_k, S_{n,k}; \sigma) \, \Delta t_k \, \big( \sigma_{n,k}^2 - \sigma^2 \big) = 0
\]

- \(S_{n,k}\): underlying price at step \(k\) on path \(n\)  
- \(\sigma_{n,k}^2 = \frac{(\ln S_{n,k+1} - \ln S_{n,k})^2}{\Delta t_k}\): realized variance estimate  
- \(p_n\): weight of path \(n\)  
- \(K\): number of time steps in the tenor  

---

## 3. Path Weights

### (a) Equal Weights
\[
p_n = \frac{1}{N}
\]

### (b) Realized-Vol Similarity Weights
Compare realized vol of each path to market-implied vol (or target vol) with a Gaussian kernel:

\[
p_n \propto \exp\!\left(- \frac{(\hat\sigma_{n} - \sigma_{mkt})^2}{2h^2}\right)
\]

### (c) KL-Implied Weights (Weighted Monte Carlo)
Solve for weights that minimally deviate from a prior distribution \(\hat p\) while matching option market prices:

\[
\min_{p} \; D_{KL}(p||\hat p) = \sum_{n=1}^N p_n \log \frac{p_n}{\hat p_n}
\]

subject to:
- \(\sum_{n=1}^N p_n = 1, \quad p_n \ge 0\)  
- \(\sum_{n=1}^N g_{m,n} p_n = 0 \quad \text{for all instruments } m\)

where \(g_{m,n}\) is the delta-hedged P&L of instrument \(m\) on path \(n\).

---

## 4. Numerical Solution

Define the function:

\[
f(\sigma) = \sum_{n=1}^N p_n \sum_{k=1}^K e^{-rt_k} \, S_{n,k}^2 \, \Gamma^{BS}(t_k, S_{n,k}; \sigma) \, \Delta t_k \, \big( \sigma_{n,k}^2 - \sigma^2 \big)
\]

We seek \(\sigma_{BE}\) such that:

\[
f(\sigma_{BE}) = 0
\]

- **Root-finding**: Brent’s method is used for stability and robustness.  
- **Initialization**: Start with a bracket around realized volatility and market implied volatility.

---

## 5. Interpretation

- BEVL is a **Gamma-weighted realized variance**, adjusted for path weights.  
- The choice of weights determines the “forward-looking” bias:  
  - Equal → purely historical  
  - Similarity → conditioned on past similarity to current regime  
  - KL-implied → fully aligned with option market prices  

---

## 6. Applications

- Construct “virtual” volatility surfaces in markets with poor liquidity  
- Compare BEVL surface to implied vol surface → measure volatility risk premium  
- Use as inputs for exotic option pricing, scenario analysis, and stress testing  

---

## 7. References
- Dupire, B. (2006). *Functional Itô Calculus and Applications*.  
- Avellaneda, M., Friedman, C., Holmes, R., & Samperi, D. (2001). *Weighted Monte Carlo: A New Approach to Portfolio Risk Management*.  
