import numpy as np
import matplotlib.pyplot as plt

g = -9.81 # gravity, m/s^2

def time_of_flight(v0, angle):
    def y(t):
        v0y = v0 * np.sin(angle * np.pi/180)
        return v0y * t + g * t**2/2

    a, b = 0, 1
    while y(b) > 0:     # bracketing
        b *= 2

    while b-a > 0.001:  # binary search
        m = (a + b)/2
        if y(m) > 0:
            a = m
        else:
            b = m
    return (a + b)/2

#def tof(v0, angle):
#    v0y  = v0 * np.sin(angle * np.pi/180)
#    return - v0y * 2 / g

print(time_of_flight(30, 42))

def best_elevation(v0):
    def distance(v0, angle):
        v0x  = v0 * np.cos(angle * np.pi/180)
        return v0x * time_of_flight(v0, angle)

    a, b = 0, 90          # we already have the bracket
    while b - a > 0.001:  # ternary search
        m1 = a + (b - a) / 3
        m2 = b - (b - a) / 3
        if distance(v0, m1) < distance(v0, m2):
            a = m1
        else:
            b = m2
    return (a + b)/2

print(best_elevation(30))

