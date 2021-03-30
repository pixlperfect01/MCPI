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
        self.cam  = meth.vec3d(0, 0, 0)
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

    def matRotZ(self, angle):
        return meth.mat4x4([
            [math.cos(angle), math.sin(angle), 0, 0],
            [-math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def matRotX(self, angle):
        return meth.mat4x4([
            [1, 0, 0, 0],
            [0, math.cos(angle), math.sin(angle), 0],
            [0, -math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1],
        ])

    def matRotY(self, angle):
        return meth.mat4x4([
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    def on_render(self):
        self.display_surf.fill((0, 0, 0))
        tris = []
        for b in self.world.get_blocks((0, 0, 0)):
            pygame.event.poll()
            tris.extend(b.as_tris())
        tris_to_raster = []
        print("YES")
        for tri in tris:
            pygame.event.poll()
            triTrans = tri
            matRotZ = self.matRotZ(self.fTheta)
            matRotX = self.matRotX(self.fTheta*2)

            matWorld = meth.mult_mat_mat(matRotZ, meth.mat4x4([
                [1,1,1,1],
                [1,1,1,1],
                [1,1,1,1],
                [1,1,1,1]
            ]))

            triTrans = meth.tri(meth.mult_mat_vec(triTrans.p1, matWorld),
                meth.mult_mat_vec(triTrans.p2, matWorld),
                meth.mult_mat_vec(triTrans.p3, matWorld))
            print(triTrans.p1, triTrans.p2, triTrans.p3)
            # triTrans = meth.tri(meth.mult_mat_vec(triTrans.p1, matRotY),
            #     meth.mult_mat_vec(triTrans.p2, matRotX),
            #     meth.mult_mat_vec(triTrans.p3, matRotX))

            triTrans.p1.z += 3
            triTrans.p2.z += 3
            triTrans.p3.z += 3

            line1 = triTrans.p2 - triTrans.p1
            line2 = triTrans.p3 - triTrans.p1
            normal = meth.vec3d(0, 0, 0)

            normal = meth.vec3d.cross(line1, line2)

            l = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)

            normal /= l

            cam_ray = triTrans - self.cam

            if (math.vec3d.dot(normal, cam_ray)) < 0:

                light_dir = meth.vec3d(0, 0, -1)
                l = math.sqrt(light_dir.x**2 + light_dir.y**2 + light_dir.z**2)
                light_dir /= l

                dp = meth.vec3d.dot(normal, light_dir)

                triProj = meth.tri(meth.mult_mat_vec(triTrans.p1, self.proj_mat),
                    meth.mult_mat_vec(triTrans.p2, self.proj_mat),
                    meth.mult_mat_vec(triTrans.p3, self.proj_mat))

                triProj.t = dp

                triProj.p1.x = (triProj.p1.x+1)*0.5*self.width
                triProj.p2.x = (triProj.p2.x+1)*0.5*self.width
                triProj.p3.x = (triProj.p3.x+1)*0.5*self.width

                triProj.p1.y = (triProj.p1.y+1)*0.5*self.height
                triProj.p2.y = (triProj.p2.y+1)*0.5*self.height
                triProj.p3.y = (triProj.p3.y+1)*0.5*self.height

                tris_to_raster.append(triProj)

        def k(t1):
            z1 = t1.p1.z + t1.p2.z + t1.p3.z
            z1 /= 3
            return z1

        tris_to_raster = sorted(tris_to_raster, key=k, reverse=False)

        for tri in tris_to_raster:

            pygame.draw.polygon(self.display_surf, (max(255*tri.t,64), max(255*tri.t,64), max(255*tri.t,64)), [
                (tri.p1.x, tri.p1.y),
                (tri.p2.x, tri.p2.y),
                (tri.p3.x, tri.p3.y),
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
