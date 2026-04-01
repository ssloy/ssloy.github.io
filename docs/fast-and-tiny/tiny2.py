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

def trace(eye, ray, depth):
    hit,point,normal = sphere_intersect(np.array([2.8, 1.1,  7]), .9, eye, ray)
    if hit: return np.array([1., 1., .3])
    return ambient_color                                           # no intersection

width, height, depth = 640, 480, 500
ambient_color = np.array([.5]*3)
image = np.zeros((height, width, 3))

for i in range(height):
    for j in range(width):
        ray = normalized(np.array([j-width/2, i-height/2, depth]))        # emit the ray along Z axis
        image[i, j] += trace(np.zeros(3), ray, 0)

plt.imsave('result.png', image)

