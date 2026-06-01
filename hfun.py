from math import pi

def get_hfun(longitude, latitude):
    from numpy import arccos
    x, y, z = geo_to_cart(longitude, latitude)

    r = arccos(z)

    r = r * 6371.229

    return dx(r)

def get_density(longitude, latitude):
    dx = get_hfun(longitude, latitude)

    return (1.0 / (dx / 3.0))**4

def geo_to_cart(lam, phi):
    from numpy import cos, sin
    R = 1.0
    z = R * sin(phi)
    x = R * cos(lam) * cos(phi)
    y = R * sin(lam) * cos(phi)
    return (x, y, z)

def hfun(x):
   from numpy import sin
   return (95160.0 * x
         + 23760.0 * sin(2 * x)
         - 7425.0 * sin(4 * x)
         + 2200.0 * sin(6 * x)
         - 495.0 * sin(8 * x)
         + 72.0 * sin(10 * x)
         - 5.0 * sin(12 * x)) / 122880.0

hfun_min = hfun(-0.5 * pi)

def hfun_normalized(x):
   x = x * pi - 0.5 * pi
   return (hfun(x) - hfun_min) / 2.0 / abs(hfun_min)

def dx(r):
   from numpy import logical_and
   trans_center = 500.0 # 1000.0 # 500.0
   width = 500.0 # 3700.0 # 400.0
   hires = 3.0 # 10.0 # 3.0
   lowres = 15.0 # 120.0 # 15.0

   hires_mask = r < trans_center
   transition_mask = logical_and(r >= trans_center, r < (trans_center + width))
   lowres_mask = r >= (trans_center + width)

   ret = r
   ret[hires_mask] = hires
   ret[transition_mask] = (lowres - hires) * hfun_normalized((r[transition_mask] - trans_center) / width) + hires
   ret[lowres_mask] = lowres

   return ret
