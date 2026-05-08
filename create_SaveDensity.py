import numpy as np
import hfun

def cart_to_geo(x, y, z):
    from numpy import atan2, asin
    lam = atan2(y, x)
    phi = asin(z)
    return (lam, phi)

coords = np.loadtxt('SaveVertices')
coords = coords / 6371.229

longitude, latitude = cart_to_geo(coords[:,0], coords[:,1], coords[:,2])

density = hfun.get_density(longitude, latitude)

with open('SaveDensity', 'w') as f:
    for d in density:
        f.write(f'{d}\n')
