## 2. Discretization

Given \(N\) simulated or historical paths (indexed by \(n\)) and \(K\) time steps (indexed by \(k\)):

$$
\sum_{n=1}^N p_n \sum_{k=1}^K e^{-r t_k}\,
S_{n,k}^2\,\Gamma_{\mathrm{BS}}\!\big(t_k, S_{n,k}; \sigma\big)\,\Delta t_k\,
\big(\sigma_{n,k}^2 - \sigma^2\big)=0 .
$$

where  
- \(S_{n,k}\): price on path \(n\) at step \(k\)  
- \( \displaystyle \sigma_{n,k}^2 \approx \frac{\big(\ln S_{n,k+1}-\ln S_{n,k}\big)^2}{\Delta t_k}\) (set \(r_{n,k}=\ln(S_{n,k+1}/S_{n,k})\) so \(\sigma_{n,k}^2 \approx r_{n,k}^2/\Delta t_k\))  
- \(p_n\): weight of path \(n\)  
- \(K\): number of time steps in the tenor

---

## 3. Path Weights

### (a) Equal Weights
$$
p_n=\frac{1}{N}.
$$

### (b) Realized-Vol Similarity Weights
Compare each path’s realized volatility \(\hat\sigma_n\) to a reference \(\sigma_{\text{ref}}\) (e.g., recent 3M vol) with a Gaussian kernel, then normalize:
$$
\tilde w_n=\exp\!\left(-\frac{(\hat\sigma_n-\sigma_{\text{ref}})^2}{2h^2}\right),\qquad
p_n=\frac{\tilde w_n}{\sum_{j=1}^N \tilde w_j}.
$$

*(等价地也可在“方差空间”做：把 \(\hat\sigma\) 全部换成 \(\hat v=\hat\sigma^2\)，\(\sigma_{\text{ref}}\) 换成 \(v_{\text{ref}}\)。)*

### (c) KL-Implied Historical Weights (Weighted Monte Carlo)

Minimize KL divergence to a prior \(\hat p\) while enforcing market constraints:
$$
\min_{p\in\Delta_N}\;\sum_{n=1}^N p_n\log\frac{p_n}{\hat p_n}
\quad\text{s.t.}\quad
\sum_{n=1}^N g_{m,n}\,p_n=0\;\;(m=1,\dots,M),
$$
where \(g_{m,n}\) is delta-hedged P\&L of instrument \(m\) on path \(n\) computed with market IVs.
This yields the exponential-tilting form
$$
p_n^\star(\lambda)=
\frac{\hat p_n\,\exp\!\big(-\lambda^\top g_n\big)}
{\sum_{j=1}^N \hat p_j\,\exp\!\big(-\lambda^\top g_j\big)},
\qquad g_n=(g_{1,n},\dots,g_{M,n})^\top .
$$

---

## 4. Dollar Gamma under Black–Scholes

For \(\tau=T-t\),
$$
S^2\Gamma_{\mathrm{BS}}(t,S;\sigma)
= e^{-q\,\tau}\,\frac{S\,\phi(d_1)}{\sigma\sqrt{\tau}},
\qquad
d_1=\frac{\ln(S/K)+(r-q+\tfrac12\sigma^2)\tau}{\sigma\sqrt{\tau}},
$$
where \(\phi(\cdot)\) is the standard normal pdf.

---

## 5. BEVL Definition (continuous form)

$$
\mathbb{E}\!\left[\int_0^T e^{-rt}\,S_t^2\,
\Gamma_{\mathrm{BS}}(t,S_t;\sigma_{BE})\,
\big(\sigma_t^2-\sigma_{BE}^2\big)\,dt\right]=0.
$$
