import numpy as np

class vec3d:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.w = 1
        self.t = 0
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    @staticmethod
    def cross(a, b):
        o = vec3d(0, 0, 0)
        o.x = a.y * b.z - a.z * b.y
        o.y = a.z * b.x - a.x * b.z
        o.z = a.x * b.y - a.y * b.x
        return o
    @staticmethod
    def dot(a, b):
        return a.x*b.x + a.y*b.y * a.z*b.z
    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        self.z += o.z
        return self
    def __imul__(self, o):
        self.x *= o
        self.y *= o
        self.z *= o
        return self
    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
        self.z -= o.z
        return self
    def __itruediv__(self, o):
        self.x /= o
        self.y /= o
        self.z /= o
        return self
    def __add__(self, o):
        a = vec3d(self.x, self.y, self.z)
        a.x += o.x
        a.y += o.y
        a.z += o.z
        return a
    def __mul__(self, o):
        a = vec3d(self.x, self.y, self.z)
        a.x *= o
        a.y *= o
        a.z *= o
        return a
    def __sub__(self, o):
        a = vec3d(self.x, self.y, self.z)
        a.x -= o.x
        a.y -= o.y
        a.z -= o.z
        return a

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
    v = vec3d(0, 0, 0)
    v.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + i.w * m.m[3][0]
    v.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + i.w * m.m[3][1]
    v.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + i.w * m.m[3][2]
    v.w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + i.w * m.m[3][3]
    return v

def mult_mat_mat(m1, m2):
    matrix = mat4x4([[0]*4]*4)
    for c in range(4):
        for r in range(4):
            matrix.m[r][c] = m1.m[r][0] * m2.m[0][c] + m1.m[r][1] * m2.m[1][c] + m1.m[r][2] * m2.m[2][c] + m1.m[r][3] * m2.m[3][c]
    return matrix
