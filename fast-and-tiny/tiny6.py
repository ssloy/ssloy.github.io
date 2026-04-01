import numpy as np
import matplotlib.pyplot as plt

def box_intersect(bmin, bmax, ray_origin, ray_direction):
    for i in range(3): # for each coordinate axis
        if np.abs(ray_direction[i])<1e-3: continue # avoid division by zero if the ray is parallel to the plane
        normal = np.zeros(3)                       # here we test against 3 planes (instead of 6), i.e.
        normal[i] = -np.sign(ray_direction[i])     # no rendering from the inside of a box
        d = ((bmin[i] if ray_direction[i]>0 else bmax[i]) - ray_origin[i])/ray_direction[i]
        point = ray_origin + ray_direction*d       # intersection between the ray and the plane
        if (d>0 and point[(i+1)%3] > bmin[(i+1)%3] and point[(i+1)%3] < bmax[(i+1)%3] and # check whether the intersection lies
                    point[(i+2)%3] > bmin[(i+2)%3] and point[(i+2)%3] < bmax[(i+2)%3]):   # in the actual facet
            return True,point,normal
    return False,None,None # no intersection

def sphere_intersect(center, radius, ray_origin, ray_direction):
    proj = np.dot(ray_direction, center-ray_origin)
    delta = radius**2 + proj**2 - np.dot((center-ray_origin),(center-ray_origin))
    if delta>0 and (t:=proj - np.sqrt(delta)) > 0: # the smallest root suffices (one-sided walls, no rendering from the inside of a sphere)
        point = ray_origin + t * ray_direction
        return True,point,(point-center)/radius    # we have a hit, intersection point, surface normal at the point
    return False,None,None # no intersection

def normalized(vector):
    return vector / np.linalg.norm(vector)

def reflect(vector, normal):
    return normalized(vector - 2*np.dot(vector, normal)*normal)

def scene_intersect(ray_origin, ray_direction):
    nearest = np.inf                             # the (squared) distance from the ray origin to the nearest point in the scene
    point,normal,color,hot = None,None,None,None # the information about the intersection point we want to return
    for o in [ {'center': np.array([  6,   0,  7]), 'radius':  2, 'color': np.array([1., .4, .6]), 'hot': False}, # description of the scene:
               {'center': np.array([2.8, 1.1,  7]), 'radius': .9, 'color': np.array([1., 1., .3]), 'hot': False}, # two spheres
               {'center': np.array([  5, -10, -7]), 'radius':  8, 'color': np.array([1., 1., 1.]), 'hot': True},  # one of the spheres is "hot" (incandescent)
               {'min': np.array([3, -4, 11]), 'max': np.array([ 7,   2, 13]), 'color': np.array([.4, .7, 1.]), 'hot': False},
               {'min': np.array([0,  2,  6]), 'max': np.array([11, 2.2, 16]), 'color': np.array([.6, .7, .6]), 'hot': False} ]:
        if 'center' in o: # is it a sphere or a box?
            hit,p,n = sphere_intersect(o['center'], o['radius'], ray_origin, ray_direction)
        else:
            hit,p,n = box_intersect(o['min'], o['max'], ray_origin, ray_direction)
        if hit and (d2:=np.dot(p-ray_origin, p-ray_origin))<nearest: # we have encountered the closest point so far
            nearest,point,normal,color,hot = d2,p,n,o['color'],o['hot']
    return nearest<np.inf, point, normal, color, hot # hit or not, intersection point, normal at the point, color of the object

def trace(eye, ray, depth):
    hit,point,normal,color,hot = scene_intersect(eye, ray)             # find closest point along the ray
    if hot: return color
    if hit and depth+1<maxdepth:
        return color * trace(point, reflect(ray, normal), depth+1) # accumulate color along the reflected ray
    return ambient_color                                           # no intersection

width, height, depth = 640, 480, 500
azimuth, ambient_color = 30*np.pi/180, np.array([.5]*3)
image = np.zeros((height, width, 3))
maxdepth = 3

for i in range(height):
    for j in range(width):
        ray = normalized(np.array([j-width/2, i-height/2, depth]))        # emit the ray along Z axis
        ray[0],ray[2] = (np.cos(azimuth)*ray[0] + np.sin(azimuth)*ray[2], # and then rotate it 30 degrees around Y axis
                        -np.sin(azimuth)*ray[0] + np.cos(azimuth)*ray[2])
        image[i, j] += trace(np.zeros(3), ray, 0)
    print("%d/%d" % (i + 1, height))

plt.imsave('result6.png', image)

