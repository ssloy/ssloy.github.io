# Petit bateau sur un ruisseau

On considère un ruisseau représenté dans le plan par un domaine du repère orthonormé $(O,x,y)$, les distances s'y mesurent en *toises*.
Deux ponts traversent ce ruisseau ; ils sont modélisés par les segments $[P_1,P_2]$ et $[P_3,P_4]$ définis par :

$$
P_1 = \left(\tfrac{3}{4},0\right) \qquad P_2 = \left(\tfrac{5}{4},0\right)
$$

and

$$
P_3 = \left(0,\tfrac{3}{4}\right) \qquad P_4 = \left(0,\tfrac{5}{4}\right).
$$

![](river/river.png)

Sur chacun des deux ponts se tient un garçon, Arthur et Basile. Ils s’amusent à déposer un petit bateau à la surface de l’eau et observent sa trajectoire sous l’effet du courant du ruisseau.

On suppose [connue](river/stream.py) une fonction `current(x,y)` qui, à tout point $(x,y)$ du plan, associe le vecteur vitesse du courant en ce point (celui-ci étant nul en dehors du ruisseau).
La vitesse est donnée en toises par seconde.

## Problème posé

Étant donnée la position de Basile sur le pont $[P_3,P_4]$, décrite par ses coordonnées $(B_x, B_y)$, on souhaite déterminer la position d'Arthur sur le pont $[P_1,P_2]$, décrite par $(A_x, A_y)$,
telle que le petit bateau lâché en $(A_x, A_y)$ soit transporté par le courant et arrive à la position $(B_x, B_y)$ avec une précision d'une ligne (pour rappel, il y a 864 lignes dans une toise).

## Questions

1. Modéliser mathématiquement la trajectoire du bateau à l’aide d’une équation différentielle dépendant de la fonction `current(x,y)`.
2. Formuler précisément le problème de recherche de $(A_x, A_y)$ comme un problème de recherche de racine.
3. Proposer une méthode numérique ainsi que son implémentation permettant de déterminer la position recherchée sur le segment $[P_1,P_2]$.
Le programme doit prendre en entrée un point $(B_x, B_y)$ et afficher à l’écran $(A_x, A_y)$ ainsi que le temps de trajet du petit bateau entre Arthur et Basile.

On veillera à expliciter clairement les hypothèses de modélisation ainsi que les choix numériques effectués.
Le raisonnement est plus important que les résultats : il est essentiel de rédiger soigneusement pour obtenir au moins une partie des points.

