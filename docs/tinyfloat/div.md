---
title: Division
---

$$
\begin{align}
a &= a_m \cdot 2^{a_e - 23}\\
b &= b_m \cdot 2^{b_e - 23}
\end{align}
$$


$$
a/b = \frac{a_m}{b_m} \cdot 2^{(a_e - b_e + 23) - 23}
$$


$$
\begin{align}
q &:= \left\lfloor \frac{a_m}{b_m} \right\rfloor\\
r &:= a_m \mod b_m\\
\frac{a_m}{b_m} &= q + \frac{r}{b_m}
\end{align}
$$

$$
a/b = \left(q + \frac{r}{b_m} \right) \cdot 2^{(a_e - b_e + 23) - 23}
$$


--8<-- "comments.html"
