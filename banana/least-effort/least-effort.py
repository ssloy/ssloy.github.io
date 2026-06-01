import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

g     = -9.81 # gravity, m/s^2
speed = 30    # initial speed (m/s)
x_star, y_star = 34, 23

def simulate(vx, vy):
    x, y = 0, 0   # current state
    dt = .001
    xs, ys = [x], [y]
    while x < x_star:
        x += dt * vx
        y += dt * vy
        vy += g * dt
        xs.append(x)
        ys.append(y)
    plt.plot(xs, ys, alpha=.04, zorder=2, color='gray')
    return xs, ys

def bisection(vx):
    a, b = 10, 20
    while simulate(vx, b)[1][-1] < y_star: # bracketing
        b *= 2

    while b - a > 0.01: # binary search
        m = (a + b)/2
        if simulate(vx, m)[1][-1] < y_star:
            a = m
        else:
            b = m
    return (a + b)/2

def ternary_search():
    a, b = 3, 50      # we already have the bracket
    while b - a > .5:  # ternary search
        m1 = a + (b - a) / 3
        m2 = b - (b - a) / 3
        vy1 = bisection(m1)
        vy2 = bisection(m2)
        e1 =  np.sqrt(m1*m1 + vy1*vy1)
        e2 =  np.sqrt(m2*m2 + vy2*vy2)
        if e1 > e2:
            a = m1
        else:
            b = m2
        print(e1, e2)
        xs, ys = simulate(m1, vy1)
        plt.plot(xs, ys, alpha=.6, color=cmap(norm(e1)))
        xs, ys = simulate(m2, vy2)
        plt.plot(xs, ys, alpha=.6, color=cmap(norm(e2)))
    r = (a+b)/2
    return r, bisection(r)

plt.figure(figsize=(16, 9))
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['text.usetex'] = True

plt.rc('font', size=24)
plt.title('The lazy ape is not so lazy')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.scatter(x_star, y_star)

vmin, vmax = 25.06, 26
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
cmap = cm.RdYlGn.reversed()


vx, vy = ternary_search()
print(vx,vy)

xs,ys = simulate(vx,vy)
plt.plot(xs, ys, linewidth=2, color='k')


plt.scatter(x_star, y_star, zorder=-1)

plt.xlabel("$x$")
plt.ylabel("$y$")
plt.ylim(0, 35)
plt.gca().set_aspect('equal', 'box')
plt.savefig("least-effort.png")
plt.show()


# diff(vx*y_star/x_star - g/2*(x_star/vx), vx);
