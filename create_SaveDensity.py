import numpy as np
import math

def hfun(x):
   return (95160.0 * x
         + 23760.0 * math.sin(2 * x)
         - 7425.0 * math.sin(4 * x)
         + 2200.0 * math.sin(6 * x)
         - 495.0 * math.sin(8 * x)
         + 72.0 * math.sin(10 * x)
         - 5.0 * math.sin(12 * x)) / 122880.0

hfun_min = hfun(-0.5 * math.pi)

def hfun_normalized(x):
   x = x * math.pi - 0.5 * math.pi
   return (hfun(x) - hfun_min) / 2.0 / abs(hfun_min)

def dx(r, hfun_min):
   trans_center = 500.0 # 1000.0 # 500.0
   width = 500.0 # 3700.0 # 400.0
   hires = 3.0 # 10.0 # 3.0
   lowres = 15.0 # 120.0 # 15.0
   if r < trans_center:
      return hires
   elif r < (trans_center + width):
      rr = (r - trans_center) / width
      return (lowres - hires) * hfun_normalized(rr) + hires
   else:
      return lowres

def get_hfun(x, y, z):
    r = np.arccos(z)

    r = r * 6371.220

    return dx(r, hfun_min)

def get_density(x, y, z):
    dx = get_hfun(x, y, z)

    return (1.0 / (dx / 3.0))**4

coords = np.loadtxt('SaveVertices')
coords = coords / 6371.22

get_density_vectorized = np.vectorize(get_density)
density = get_density_vectorized(coords[:,0], coords[:,1], coords[:,2])

with open('SaveDensity', 'w') as f:
    for d in density:
        f.write(f'{d}\n')
