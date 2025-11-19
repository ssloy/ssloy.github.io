---
title: Multiplicaton
---


$$
\begin{align}
h(n) &:= \left\lfloor\frac{n}{2^{12}}\right\rfloor \\
l(n) &:= n \mod 2^{12}\\
\end{align}
$$

$$
\begin{align}
a_m &=  h(a_m) 2^{12} + l(a_m) \\
b_m &=  h(b_m) 2^{12} + l(b_m)
\end{align}
$$

$$
\begin{align}
a_m b_m &=  \left(h(a_m) 2^{12} + l(a_m)\right) \left(h(b_m) 2^{12} + l(b_m)\right) \\
&= h(a_m) h(b_m) 2^{24} + l(a_m) l(b_m) + (h(a_m) l(b_m) + l(a_m) h(b_m)) 2^{12} \\
&= \Big( h(a_m) h(b_m) + h(h(a_m) l(b_m)) + h(l(a_m) h(b_m)) \Big) 2^{24} + \\
&\qquad l(a_m) l(b_m) + \big( l(h(a_m) l(b_m)) + l(l(a_m) h(b_m))\big) 2^{12}
\end{align}
$$

--8<-- "comments.html"
