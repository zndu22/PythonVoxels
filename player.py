import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)
        self.vel = glm.vec3()

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        forwardXZ = glm.vec3(glm.cos(self.yaw), 0, glm.sin(self.yaw))
        leftXZ = glm.cross(forwardXZ, glm.vec3(0, 1, 0))
        solid = self.app.scene.world.voxel_handler.is_solid
        # hitbox
        h = [
            solid(self.position + glm.vec3(0.25, 0.1, 0.25)), solid(self.position + glm.vec3(-0.25, 0.1, 0.25)),
            solid(self.position + glm.vec3(-0.25, 0.1, -0.25)), solid(self.position + glm.vec3(0.25, 0.1, -0.25)),

            solid(self.position + glm.vec3(0.25, -1.5, 0.25)), solid(self.position + glm.vec3(0.25, -1.5, -0.25)),
            solid(self.position + glm.vec3(-0.25, -1.5, -0.25)), solid(self.position + glm.vec3(0.25, -1.5, -0.25)),

            solid(self.position + glm.vec3(0.25, -1.7, 0.25)), solid(self.position + glm.vec3(0.25, -1.7, -0.25)),
            solid(self.position + glm.vec3(-0.25, -1.7, -0.25)), solid(self.position + glm.vec3(0.25, -1.7, -0.25))
        ]

        if h[8] or h[9] or h[10] or h[11]:
            self.vel.y = 0
        else:
            self.vel.y += GRAVITY
        
        if key_state[pg.K_w]:
            self.vel += forwardXZ * PLAYER_SPEED
        if key_state[pg.K_s]:
            self.vel -= forwardXZ * PLAYER_SPEED
        if key_state[pg.K_a]:
            self.vel -= leftXZ * PLAYER_SPEED
        if key_state[pg.K_d]:
            self.vel += leftXZ * PLAYER_SPEED
        if key_state[pg.K_SPACE]:
            self.vel -= GRAVITY * 5

        self.position += self.vel

        if h[0] or h[1] or h[4] or h[5]:
            self.position.x -= self.vel.x * 1.01

        self.vel *= glm.vec3(0.1, 1, 0.1)
