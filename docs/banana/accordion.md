# Embouteillages accordéon

Dans ce sujet, on s’intéresse à l’apparition spontanée de bouchons dits *accordéon* sur une route sans obstacle ni intersection.

L’objectif est de modéliser un ensemble de conducteurs « moyens », c’est-à-dire prudents et respectueux du code de la route. Chaque conducteur adapte sa vitesse :

- à la distance qui le sépare de la voiture située devant lui ;
- à une vitesse maximale autorisée ;
- tout en cherchant à conserver un trafic fluide et confortable.

Même avec des conducteurs parfaitement raisonnables, on observe expérimentalement l’apparition d’ondes de ralentissement et de bouchons spontanés. Le but du sujet est d’étudier numériquement ce phénomène.

---

## Modèle

On considère une route circulaire de longueur $L = 1024\ \text{m}$ sur laquelle circulent $N = 32$ voitures numérotées de \(1\) à \(N\).

On note :

- \(x_i(t)\) la position de la voiture \(i\) ;
- \(v_i(t)\) sa vitesse ;
- \(a_i(t)\) son accélération.

La dynamique du système est donnée par :

$$
\left\{
\begin{array}{ll}
\displaystyle \frac{d}{dt}x_i(t) = v_i(t),\\[1em]
\displaystyle \frac{d}{dt}v_i(t) = a_i(t).
\end{array}
\right.
$$

L’accélération est une fonction connue qui dépend de la vitesse actuelle, de la vitesse maximale autorisée \(v_{\max}\) et
de la distance \(s_i(t)\) séparant la voiture \(i\) de la voiture située devant elle.

Cette distance est définie par :

$$
s_i(t) =
\left\{
\begin{array}{ll}
x_{i+1}(t) - x_i(t)
& \text{si } x_{i+1}(t) > x_i(t),\\[0.5em]
x_{i+1}(t) - x_i(t) + L
& \text{sinon}.
\end{array}
\right.
$$

On considère ensuite le modèle d’accélération :

$$
a_i(t)
=
2 - 2\left(
\frac{s_i(t)\,v_i(t)}
{v_{\max}\,(s_i(t)-5)}
\right)^4.
$$

On prendra garde aux unités, dans ce modèle les positions sont exprimées en mètres, les vitesses en m/s et le temps en secondes.

---

## Partie I — Mise en place de la simulation

On fixe :

$$
v_{\max} = 130\ \text{km/h}.
$$

Écrire un programme Python simulant le trafic sur la route circulaire pendant $T = 256\ \text{s}.$

Au temps initial les voitures sont régulièrement espacées ; toutes les voitures roulent à \(0.75\,v_{\max}\),
sauf une voiture dont la vitesse initiale est fixée à \(0.375\,v_{\max}\).

Utiliser un schéma d’Euler explicite avec :

$$
dt = 0.01.
$$

Le schéma numérique est donc :

$$
\begin{align*}
x_i &\leftarrow x_i + dt\,v_i,\\
v_i &\leftarrow v_i + dt\,a_i.
\end{align*}
$$

Tracer les trajectoires $x_i(t)$ de toutes les voitures sur un même graphique.
Décrire qualitativement s'il s'agit d'un trafic fluide ou bien un trafic instable.

---

## Partie II — Mesure du bruit du trafic et vitesse moyenne

On définit le *bruit du trafic* par :

$$
Q
=
\frac{1}{NT}
\int_0^T
\sum_{i=1}^N
(a_i(t))^2\,dt.
$$

Cette quantité mesure l’importance des accélérations et freinages répétés, et donc également  l’inconfort des conducteurs et l’instabilité globale du trafic.

On définit également la vitesse moyenne :

$$
\bar v
=
\frac{1}{NT}
\int_0^T
\sum_{i=1}^N
v_i(t)\,dt.
$$

Faire varier $v_{\max} \in [50,130]\ \text{km/h}$ et tracer :

- \(Q(v_{\max})\) ;
- \(\bar v(v_{\max})\).

Commenter les graphes obtenus :

- observe-t-on un seuil d’apparition des bouchons ?
- le trafic reste-t-il stable pour toutes les vitesses ?
- une vitesse maximale élevée garantit-elle un trafic efficace ?

---

## Partie III — Optimisation

On souhaite maintenant choisir une vitesse maximale « optimale ».  On introduit le score :

$$
J(v_{\max}) = \bar v - Q,
$$

qui favorise un trafic rapide, mais pénalise les fortes accélérations et freinages.

Déterminer numériquement la valeur de \(v_{\max}\) maximisant \(J\) dans l’intervalle $v_{\max} \in [50,130]\ \text{km/h}$.
Tracer également le graphe de \(J(v_{\max})\).

Interpréter le compromis obtenu :
pourquoi la vitesse maximale optimale n’est-elle pas nécessairement la plus grande possible ?

---

## Partie IV — Influence du nombre de voitures

On fixe maintenant $N = 64$. Étudier l’influence du nombre de voitures (toujours dans le même intervalle $v_{max} \in [50, 130]$ km/h) sur :

- la stabilité du trafic  ;
- l’apparition des bouchons ;
- le bruit du trafic \(Q\).

Comparer les résultats obtenus avec le cas \(N = 32\).

---

# Partie V — Bonus (difficile)

Expliquer pourquoi les bouchons semblent se propager vers l’arrière alors que les voitures roulent vers l’avant.

*Astuce :* penser à une onde de densité plutôt qu’au mouvement individuel des véhicules.



