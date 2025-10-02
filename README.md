# BEVL Toolkit — Break-Even Volatility Surface Construction

**Break-Even Volatility (BEVL)** is the volatility under which the **expected P&L of a delta-hedged option is zero** (Dupire, 2006).  
Unlike implied volatility (IV), which comes from option market prices, BEVL is constructed from **historical paths with Gamma weighting**.  
This provides a “virtual volatility surface” that serves as a fair benchmark for skew and risk premium analysis.

---

## Features
- Build BEVL surfaces from **historical paths** or **simulations**
- **Multiple weighting schemes**:
  - Equal weights
  - Realized-vol similarity weights (Gaussian kernel)
  - KL-implied weights (Weighted Monte Carlo calibration)
- Gamma-weighted integration across paths and strikes
- Brent root-finding for BEVL at each strike/tenor
- Example: S&P500 1M BEVL surface

---

## Methodology

### 1. Continuous Definition
Break-even volatility $\sigma_{BE}$ is defined as the volatility under which the expected P&L of a delta-hedged option equals zero:
$$
\mathbb{E}\left[\int_{0}^{T}e^{-rt}S_t^2\Gamma_{\mathrm{BS}}(t,S_t;\sigma_{BE})(\sigma_t^2-\sigma_{BE}^2)dt\right]=0
$$


where:

- $\Gamma_{\text{BS}}$ = Black–Scholes Gamma under constant volatility assumption  
- $\sigma_t^2$ = realized variance at time $t$

---

## 2. Discretization

With $N$ historical/simulated paths ($n$) and $K$ time steps ($k$):

$$
\sum_{n=1}^N p_n \sum_{k=1}^K e^{-rt_k} S_{n,k}^2 \, \Gamma_{\text{BS}}(t_k, S_{n,k}; \sigma) \, \Delta t_k \, \big( \sigma_{n,k}^2 - \sigma^2 \big) = 0
$$

where:

- $S_{n,k}$ = price on path $n$ at step $k$  
- Realized variance estimate:
  $$
  \sigma_{n,k}^2 \approx \frac{(\ln S_{n,k+1} - \ln S_{n,k})^2}{\Delta t_k}
  $$
- $p_n$ = weight of path $n$  
- Solve via **root-finding in $\sigma$**

---

## 3. Black–Scholes Dollar Gamma

For $\tau = T - t$:

$$
S^2 \Gamma_{\text{BS}}(t, S; \sigma) \;=\; e^{-q\tau} \, \frac{S \, \phi(d_1)}{\sigma \sqrt{\tau}},
$$

where:

- $d_1 = \dfrac{\ln(S/K) + (r - q + \tfrac{1}{2}\sigma^2)\tau}{\sigma \sqrt{\tau}}$  
- $\phi(\cdot)$ = standard normal PDF

---

## 4. Path Weights

We consider different schemes for weighting paths:

### (a) Equal Weights

$$
p_n = \frac{1}{N}
$$

---

### (b) Realized-Vol Similarity Weights

Compare each path’s realized volatility $\hat{\sigma}_n$ to a reference volatility $\sigma_{\text{ref}}$:

$$
\tilde{w}_n = \exp\!\left(-\frac{(\hat{\sigma}_n - \sigma_{\text{ref}})^2}{2h^2}\right),
\qquad
p_n = \frac{\tilde{w}_n}{\sum_{j=1}^N \tilde{w}_j}
$$

---

### (c) KL-Implied Historical Weights (Weighted Monte Carlo)

Minimize KL divergence to a prior $\hat{p}_n$ subject to calibration constraints:

$$
\min_{p \in \Delta_N} \sum_{n=1}^N p_n \log \frac{p_n}{\hat{p}_n}
$$

subject to:

$$
\sum_{n=1}^N g_{m,n} p_n = 0, 
\quad m = 1, \dots, M
$$

where $g_{m,n}$ = delta-hedged P\&L of instrument $m$ on path $n$ under market implied volatility.

---

## Use Cases
- **Compare BEVL vs IV** → detect volatility risk premium  
- **Fair skew estimation** → construct “virtual” skew curve without IV noise  
- **Risk management** → Gamma-weighted realized variance reflects true hedging risk  
- **Research** → methodology for linking realized & implied volatility  

---

## Example
```bash
python examples/run_example.py --csv data/SPX_sample.csv --tenor_days 21 --strikes 0.9 1.0 1.1
