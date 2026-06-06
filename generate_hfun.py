#!/usr/bin/env python

import numpy as np
import hfun

lats = np.linspace(-np.pi/2.0, np.pi/2.0, num=2048, endpoint=True)
lons = np.linspace(-np.pi, np.pi, num=4096, endpoint=True)
latgrid, longrid = np.meshgrid(lats, lons)

nlats = lats.size
nlons = lons.size
npts = nlats * nlons

distance = hfun.get_hfun(longrid, latgrid)

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
    for d in distance.flatten():
        f.write(f'{d}\n')
