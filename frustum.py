from settings import *

class Frustum:
    def __init__(self, camera):
        self.cam = camera
        
    def is_on_frustum(self, chunk):
        # vector to sphere center
        sphere_vec = chunk.center - self.cam.position

        # outside NEAR or FAR plane?
        sz = glm.dot(sphere_vec, self.cam.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS)
            return False
        
        return True