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

def get_hfun(lon, lat):
    # x = np.cos(lat) * np.cos(lon)
    # y = np.cos(lat) * np.sin(lon)
    z = np.sin(lat)

    r = np.arccos(z)

    r = r * 6371.229

    return dx(r, hfun_min)

lats = np.linspace(-np.pi/2.0, np.pi/2.0, num=10, endpoint=True)
lons = np.linspace(-np.pi, np.pi, num=20, endpoint=True)
latgrid, longrid = np.meshgrid(lats, lons)

nlats = lats.size
nlons = lons.size
npts = nlats * nlons

eval_lats = [lat for lat in latgrid.flatten()]
eval_lons = [lon for lon in longrid.flatten()]

get_hfun_vec = np.vectorize(get_hfun)
distance = get_hfun_vec(eval_lons, eval_lats)

with open('HFUN.msh', 'w') as f:
    f.write('MSHID=3;ellipsoid-grid\n')
    f.write('NDIMS=2\n')
    f.write(f'COORD=1;{nlons}\n')
    for lon in lons:
        f.write(f'{lon}\n')
    f.write(f'COORD=2;{nlats}\n')
    for lat in lats:
        f.write(f'{lat}\n')

    f.write(f'VALUE={npts}; 1\n')
    for d in distance:
        f.write(f'{d}\n')
