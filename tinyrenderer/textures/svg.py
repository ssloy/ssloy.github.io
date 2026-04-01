import numpy as np
import svgwrite

def hermite_curve(P0, P1, N0, N1, n=50):
    """Compute cubic Hermite curve points from endpoints and normals."""
    # Tangents from normals (simple perpendicular in XY plane)
    T0 = np.array([-N0[1], N0[0], 0])
    T1 = np.array([-N1[1], N1[0], 0])
    
    t = np.linspace(0,1,n)[:,None]
    h00 = 2*t**3 - 3*t**2 + 1
    h01 = -2*t**3 + 3*t**2
    h10 = t**3 - 2*t**2 + t
    h11 = t**3 - t**2
    C = h00*P0 + h01*P1 + h10*T0 + h11*T1
    return C

def project(P):
    """Orthographic projection from 3D to 2D (XY plane)."""
    return P[:2]

# Triangle vertices
V0 = np.array([50,50,0])
V1 = np.array([150,50,0])
V2 = np.array([100,150,0])

# Normals at vertices (length controls tangent magnitude)
N0 = np.array([0,1,0])
N1 = np.array([0,1,0])
N2 = np.array([0,-1,0])

# Triangle edges
edges = [
    (V0,V1,N0,N1),
    (V1,V2,N1,N2),
    (V2,V0,N2,N0)
]

# Create SVG
dwg = svgwrite.Drawing('curved_triangle.svg', size=(200,200))

# Draw edges
for P0,P1,N0,N1 in edges:
    C = hermite_curve(P0,P1,N0,N1, n=50)
    points = [tuple(map(float, project(p))) for p in C]
    dwg.add(dwg.polyline(points, stroke='black', fill='none', stroke_width=2))

# Draw vertices and normals
for V,N in zip([V0,V1,V2],[N0,N1,N2]):
    dwg.add(dwg.circle(center=tuple(map(float, project(V))), r=3, fill='red'))
    end = project(V + N*20)  # scale normal for visibility
    dwg.add(dwg.line(start=tuple(map(float, project(V))),
                     end=tuple(map(float, end)),
                     stroke='blue', stroke_width=1))

dwg.save()

