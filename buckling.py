import numpy as np

def column(E, L, I):
    n = 4 # both ends fixed

    F = n * np.pi ** 2 * E * I / L ** 2
    return F

def newtons_to_kg(N):
    return N * 0.101972

def area_moment(outside_diameter, thickness):
    do = outside_diameter
    di = do - 2*thickness
    Iy = np.pi * (do**4 - di**4)/64
    return Iy

def do_column(E, L,  od, thickness):
    Iy = area_moment(od, thickness)
    N = column(E, L, Iy)
    return newtons_to_kg(N)


E = 200e9 # Pa
