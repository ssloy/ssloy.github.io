import numpy as np
import matplotlib.pyplot as plt

def sphere_intersect(center, radius, ray_origin, ray_direction):
    proj = np.dot(ray_direction, center-ray_origin)
    delta = radius**2 + proj**2 - np.dot((center-ray_origin),(center-ray_origin))
    if delta>0 and (t:=proj - np.sqrt(delta)) > 0: # the smallest root suffices (one-sided walls, no rendering from the inside of a sphere)
        point = ray_origin + t * ray_direction
        return True,point,(point-center)/radius    # we have a hit, intersection point, surface normal at the point
    return False,None,None # no intersection

def normalized(vector):
    return vector / np.linalg.norm(vector)

def scene_intersect(ray_origin, ray_direction):
    nearest = np.inf                             # the (squared) distance from the ray origin to the nearest point in the scene
    point,normal,color = None,None,None # the information about the intersection point we want to return
    for o in [ {'center': np.array([  6,   0,  7]), 'radius':  2, 'color': np.array([1., .4, .6])},  # description of the scene:
               {'center': np.array([2.8, 1.1,  7]), 'radius': .9, 'color': np.array([1., 1., .3])}]: # two spheres
        hit,p,n = sphere_intersect(o['center'], o['radius'], ray_origin, ray_direction)
        if hit and (d2:=np.dot(p-ray_origin, p-ray_origin))<nearest: # we have encountered the closest point so far
            nearest,point,normal,color = d2,p,n,o['color']
    return nearest<np.inf, point, normal, color # hit or not, intersection point, normal at the point, color of the object

def trace(eye, ray, depth):
    hit,point,normal,color = scene_intersect(eye, ray)             # find closest point along the ray
    if hit: return color
    return ambient_color                                           # no intersection

width, height, depth = 640, 480, 500
azimuth, ambient_color = 30*np.pi/180, np.array([.5]*3)
image = np.zeros((height, width, 3))

for i in range(height):
    for j in range(width):
        ray = normalized(np.array([j-width/2, i-height/2, depth]))        # emit the ray along Z axis
        ray[0],ray[2] = (np.cos(azimuth)*ray[0] + np.sin(azimuth)*ray[2], # and then rotate it 30 degrees around Y axis
                        -np.sin(azimuth)*ray[0] + np.cos(azimuth)*ray[2])
        image[i, j] += trace(np.zeros(3), ray, 0)

plt.imsave('result.png', image)

