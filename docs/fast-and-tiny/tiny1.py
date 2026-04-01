import numpy as np
import matplotlib.pyplot as plt

def sphere_intersect(center, radius, ray_origin, ray_direction):
    proj = np.dot(ray_direction, center-ray_origin)
    delta = radius**2 + proj**2 - np.dot((center-ray_origin),(center-ray_origin))
    if delta>0 and (t:=proj - np.sqrt(delta)) > 0: # the smallest root suffices (one-sided walls, no rendering from the inside of a sphere)
        point = ray_origin + t * ray_direction
        return True,point,(point-center)/radius    # we have a hit, intersection point, surface normal at the point
    return False,None,None # no intersection

width, height = 640, 480
image = np.zeros((height, width, 3))

for i in range(height):
    for j in range(width):
        image[i,j] = np.array([j/width, i/height, 0])

plt.imsave('result.png', image)

center,radius = np.array([6, 0, 7]), 2
eye,ray = np.zeros(3), np.array([.5, 0, 0.866])
hit, point, normal = sphere_intersect(center, radius, eye, ray)
print(point)
