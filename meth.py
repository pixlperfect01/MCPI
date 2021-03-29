import numpy as np

class vec3d:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.t = 0

class tri:
    def __init__(self, p1, p2, p3):
        self.p1, self.p2, self.p3 = p1, p2, p3

class mesh:
    def __init__(self, tris):
        self.tris = tris

class mat4x4:
    def __init__(self, cells):
        self.m = cells

def mult_mat_vec(i, m):
    o = vec3d(0, 0, 0)
    o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0]
    o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1]
    o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2]
    w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3]
    if w != 0:
        o.x /= w
        o.y /= w
        o.z /= w
    return o
