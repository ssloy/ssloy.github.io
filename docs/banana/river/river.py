import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def current(x,y):
    def f(x, y):
        if x<-.01 or x>5.51 or y<-0.01 or y>1.01:
            return 0,0
        vortices = [[1.4030927323372038, 0.7779469895497861,  0.31732111664181495, 12.753451286971085,  1, 1.5219248898251512],
                    [2.41673573072835,   0.4036921786589822,  0.123484182230017,   24.39283282620738,   1, 0.8655341358101067],
                    [3.286840247373826,  0.10168484268088857, 0.20588551791918053, 36.07700161703913,  -1, 1.1823068700026078],
                    [1.3066814743301447, 0.35394370574110734, 0.05781273885746335, 32.477306776274915, -1, 1.8782983255570211],
                    [2.143612713064637,  0.2732795177044907,  0.19774080145395107, 1.4520393787433972, -1, 1.527401990262979 ],
                    [3.8175010568457597, 0.5422876610343721,  0.17099514514806335, 33.84242699249872,   1, 1.9044889105823875],
                    [3.779519871357598,  0.4329439511154769,  0.37069444242685295, 46.109428123494375, -1, 0.3718125317894354],
                    [3.9776302365281953, 0.787957223036232,   0.09231148593203226, 16.634759268006455,  1, 1.0154345010226322]]
        dx, dy = 1, 0
#        dx, dy = 3-y, 0
#        return dx, dy
        for v in vortices:
            xc,yc,R,omega,sign,outflow = v
            dx_c = x - xc
            dy_c = y - yc
            r2 = dx_c**2 + dy_c**2
            vortex_factor = np.exp(-r2 / R**2)
            vortex_dx = -omega * dy_c * sign + outflow*dx_c/R
            vortex_dy =  omega * dx_c * sign + outflow*dy_c/R
            dx += y*(1-y) * vortex_factor * vortex_dx
            dy += y*(1-y) * vortex_factor * vortex_dy
        return dx, dy
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    [dthetadx,dthetady],[drdx,drdy] = [[-y/r**2, x/r**2],[x/r, y/r]]
    t = theta*10/np.pi
    dtdx = dthetadx*10/np.pi
    dtdy = dthetady*10/np.pi
    w = .5 + .05*np.sin(8 * theta)
    dwdx = .05*np.cos(8 * theta)*8*dthetadx
    dwdy = .05*np.cos(8 * theta)*8*dthetady
    tau = (2*(r-1)/w + 1)/2
    dtaudx = drdx/w - (r-1)*dwdx/w**2
    dtaudy = drdy/w - (r-1)*dwdy/w**2
    return list(np.linalg.inv(np.array([[dtdx, dtdy],[dtaudx, dtaudy]])) @ np.array(f(t,tau)))

if True:
    t = np.linspace(0, 1.5, 1000)
    centerline = np.column_stack([np.cos(t*np.pi/2), np.sin(t*np.pi/2)])
    widths = .5 + .05 * np.sin(4*np.pi*t)

    tangent = np.gradient(centerline, axis=0)
    norm = np.sqrt((tangent**2).sum(axis=1))[:,None]
    tangent /= norm

    normal = np.zeros_like(tangent)
    normal[:,0] = -tangent[:,1]
    normal[:,1] = tangent[:,0]

    left_edge  = centerline + (widths/2)[:,None]*normal
    right_edge = centerline - (widths/2)[:,None]*normal

    river_poly = np.vstack([left_edge, right_edge[::-1]])

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.rcParams['text.usetex'] = True

    plt.rc('font', size=24)


    fig, ax = plt.subplots(figsize=(8,8))
    river_patch = Polygon(river_poly, closed=True, color='skyblue',alpha=.1)
    ax.add_patch(river_patch)

    t = np.linspace(0, 4.9, 50)
    tau = np.linspace(0, 1, 20)
    X = np.empty((len(tau), len(t)))
    Y = np.empty((len(tau), len(t)))
    for i in range(len(tau)):
        for j in range(len(t)):
            theta = np.pi/10*t[j]
            w = .5 + .05*np.sin(8*theta)
            r = (tau[i]-.5)*w + 1
            X[i, j] = r * np.cos(theta)
            Y[i, j] = r * np.sin(theta)

DX, DY = np.empty_like(X), np.empty_like(Y)
for i in range(len(tau)):
    for j in range(len(t)):
        DX[i, j], DY[i, j] = current(X[i, j], Y[i, j])
ax.quiver(X, Y, DX, DY, scale=16, color='teal')



def boat(x, y):
    X = []
    Y = []
    dt = .01
    cnt = 0
    while  cnt < 10000:
        X.append(x)
        Y.append(y)
        dx, dy = current(x,y)
        x += dx*dt
        y += dy*dt
        cnt += 1
    plt.plot(X,Y)
    return x,y

X = np.linspace(.75, 1.25, 10)
Y = []
for x in X:
    Y.append(boat(x,0)[1])

Y2 = [boat(x, 0)[1] for x in X]
plt.plot(X,Y)

plt.gca().set_aspect('equal', 'box')
plt.gca().set_xlabel("$x$", fontsize=32)
plt.gca().set_ylabel("$y$", fontsize=32)
plt.scatter([.75, 1.25, 0, 0], [0, 0, .75, 1.25], color='k', s=100)
plt.text(.74, 0, '$P_1$', ha='right', va='top', fontsize=24)
plt.text(1.26,0, '$P_2$', ha='left', va='top', fontsize=24)
plt.text(0, .73, '$P_3$', ha='right', va='top', fontsize=24)
plt.text(0, 1.27, '$P_4$', ha='right', va='bottom', fontsize=24)
plt.plot([0,0],[.75, 1.25], '--', linewidth=2, color='k')
plt.plot([.75, 1.25], [0,0],'--', linewidth=2, color='k')
#plt.title('Current field')
#plt.grid(color='gray', linestyle='--', linewidth=0.5)
ax.set_xlim(-.1,1.35)
ax.set_ylim(-.1,1.35)
plt.gca().set_aspect('equal', 'box')
#plt.savefig('river.png')
plt.show()

