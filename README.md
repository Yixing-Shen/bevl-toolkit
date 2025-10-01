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

```math
E \left[ \int_0^T e^{-rt} \, S_t^2 \, \Gamma_{BS}(t, S_t; \sigma_{BE}) \, (\sigma_t^2 - \sigma_{BE}^2) \, dt \right] = 0


---

### 2. Discretization
With $N$ historical/simulated paths ($n$) and $K$ time steps ($k$):
$$
\sum_{n=1}^N p_n \sum_{k=1}^K
e^{-rt_k} S_{n,k}^2 \Gamma_{\text{BS}}(t_k,S_{n,k};\sigma)\,
\Delta t_k \, (\sigma_{n,k}^2-\sigma^2) = 0
$$

- $S_{n,k}$: price on path $n$ at step $k$  
- $\displaystyle \sigma_{n,k}^2 \approx \frac{(\ln S_{n,k+1}-\ln S_{n,k})^2}{\Delta t_k}$ (realized variance estimate)  
- $p_n$: weight of path $n$  
- Solve root-finding in $\sigma$  

---

### 3. Black–Scholes Dollar Gamma
For $\tau=T-t$:
$$
S^2\Gamma_{\text{BS}}(t,S;\sigma) =
e^{-q\tau}\frac{S\phi(d_1)}{\sigma\sqrt{\tau}},\quad
d_1=\frac{\ln(S/K)+(r-q+\tfrac12\sigma^2)\tau}{\sigma\sqrt{\tau}},
$$
where $\phi(\cdot)$ is the standard normal pdf.

---

### 4. Path Weights

**(a) Equal weights**
$$
p_n=\frac{1}{N}.
$$

**(b) Realized-vol similarity weights**
Compare each path’s realized vol $\hat\sigma_n$ to reference vol $\sigma_{\text{ref}}$:
$$
\tilde w_n=\exp\!\left(-\frac{(\hat\sigma_n-\sigma_{\text{ref}})^2}{2h^2}\right),\quad
p_n=\frac{\tilde w_n}{\sum_{j=1}^N \tilde w_j}.
$$

**(c) KL-Implied Historical Weights (Weighted Monte Carlo)**  
Minimize KL divergence to a prior $\hat p$ subject to calibration constraints:
$$
\min_{p\in\Delta_N} \sum_{n=1}^N p_n \log\frac{p_n}{\hat p_n}
\quad \text{s.t.} \quad \sum_{n=1}^N g_{m,n}p_n=0, \ m=1,\dots,M,
$$
where $g_{m,n}$ is delta-hedged P&L of instrument $m$ on path $n$ under market IV.

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
