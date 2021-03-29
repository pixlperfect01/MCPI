import os
import time

import pygame
from pygame.locals import *

import meth
import mctypes as mct
from halp import cd
import math

class App:
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = 640*2, 400*2-100

    def on_init(self):
        pygame.init()
        self.fTheta = 0
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.world = mct.World()
        pygame.display.set_caption("I'll have a McPI please")
        self.a = a = self.height/float(self.width)
        self.fov = fov = 90
        self.near = near = 0.1
        self.far = far = 1000
        self.fov_rad = fov_rad = 1 / math.tan(self.fov * 0.5 / 180 * 3.14159265352)
        self.proj_mat = meth.mat4x4([
            [a*fov_rad, 0, 0, 0],
            [0, fov_rad, 0, 0],
            [0, 0, far/(far-near), 1],
            [0, 0, (-far*near) / (far-near), 0]
        ])
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self, dt):
        self.fTheta += 0.5 * dt
        self.world.on_update(dt)
    def on_render(self):
        self.display_surf.fill((0, 0, 0))
        tris = []
        for b in self.world.get_blocks((0, 0, 0)):
            tris.extend(b.as_tris())
        for tri in tris:
            triTrans = tri
            matRotZ = meth.mat4x4([
                [math.cos(self.fTheta), math.sin(self.fTheta), 0, 0],
                [-math.sin(self.fTheta), math.cos(self.fTheta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            matRotX = meth.mat4x4([
                [1, 0, 0, 0],
                [0, math.cos(self.fTheta), math.sin(self.fTheta), 0],
                [0, -math.sin(self.fTheta), math.cos(self.fTheta), 0],
                [0, 0, 0, 1],
            ])

            triTrans = meth.tri(meth.mult_mat_vec(triTrans.p1, matRotZ),
                meth.mult_mat_vec(triTrans.p2, matRotZ),
                meth.mult_mat_vec(triTrans.p3, matRotZ))

            triTrans = meth.tri(meth.mult_mat_vec(triTrans.p1, matRotX),
                meth.mult_mat_vec(triTrans.p2, matRotX),
                meth.mult_mat_vec(triTrans.p3, matRotX))

            triTrans.p1.z += 3
            triTrans.p2.z += 3
            triTrans.p3.z += 3

            normal = meth.vec3d(0, 0, 0)
            line1 = meth.vec3d(0, 0, 0)
            line2 = meth.vec3d(0, 0, 0)

            line1.x = triTrans.p2.x - triTrans.p1.x
            line1.y = triTrans.p2.y - triTrans.p1.y
            line1.z = triTrans.p2.z - triTrans.p1.z

            line2.x = triTrans.p3.x - triTrans.p1.x
            line2.y = triTrans.p3.y - triTrans.p1.y
            line2.z = triTrans.p3.z - triTrans.p1.z

            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x

            l = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)

            normal.x /= l
            normal.y /= l
            normal.z /= l

            if normal.z < 0:
                triProj = meth.tri(meth.mult_mat_vec(triTrans.p1, self.proj_mat),
                    meth.mult_mat_vec(triTrans.p2, self.proj_mat),
                    meth.mult_mat_vec(triTrans.p3, self.proj_mat))

                triProj.p1.x = (triProj.p1.x+1)*0.5*self.width
                triProj.p2.x = (triProj.p2.x+1)*0.5*self.width
                triProj.p3.x = (triProj.p3.x+1)*0.5*self.width

                triProj.p1.y = (triProj.p1.y+1)*0.5*self.height
                triProj.p2.y = (triProj.p2.y+1)*0.5*self.height
                triProj.p3.y = (triProj.p3.y+1)*0.5*self.height

                pygame.draw.polygon(self.display_surf, (255, 255, 255), [
                    (triProj.p1.x, triProj.p1.y),
                    (triProj.p2.x, triProj.p2.y),
                    (triProj.p3.x, triProj.p3.y),
                ], 1)
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False
        dt = 0
        while(self.running):
            ct = time.time()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(dt)
            self.on_render()
            dt = (ct-time.time())
        self.on_cleanup()

try:
    if __name__ == "__main__" :
    # with cd("MCPI"):
        theApp = App()
        theApp.on_execute()
except Exception as e:
    print("\u001b[31m"+e)