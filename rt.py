import random as rnd
import numpy as np
from PIL import Image
import math
from classes import *
from helpers import *
import time

def main():
    total_start = time.time()

    # set resolution and create pixel array
    for i, angle in enumerate(np.linspace(0,math.pi*4, 120)):
        start_time = time.time()

        red_x = math.cos(angle)
        red_z = math.sin(angle) - 1.5

        # create a scene
        scene = Scene()
        scene.add_light(Light(Vec3(1,.5,-1)))
        scene.add_scene_object(Sphere(Vec3(0,-4.3,-2), 4)) # blue sphere
        scene.add_scene_object(Sphere(Vec3(0,-.25,-2), 0.5, Vec3(1,1,1), reflect=1)) # white sphere
        scene.add_scene_object(Sphere(Vec3(-1,0,-2), 0.5, Vec3(1,1,0), reflect=0.25)) # yellow sphere
        # scene.add_scene_object(Sphere(Vec3(.75,0,-2), 0.3, Vec3(1,0,0))) # red sphere
        scene.add_scene_object(Sphere(Vec3(red_x,0,red_z), 0.3, Vec3(1,0,0))) # red sphere

        camera = Camera(400, 200)
        settings = {
            "hard_shadows" : True,
            "reflection" : True,
            "lambert" : True
        }
        R = Renderer(camera, scene, settings)

        # save final image
        image = Image.fromarray(R.render(num_rays=1))
        image.save(f"imgs/test{i:03}.png")

        print(f"Frame {i+1} done in {time.time() - start_time:.3f} seconds")

    print(f"Render completed in {time.time() - total_start:.3f} seconds!")

if __name__ == "__main__":
    main()