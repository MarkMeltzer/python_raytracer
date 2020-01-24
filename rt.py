import random as rnd
import numpy as np
from PIL import Image
import math
from classes import *
from helpers import *
import time

def render(scene, cam=Camera(200, 100), num_rays=25):
    pixel_array = cam.get_pixel_array()

    # iterate over all pixels
    for screen_y, world_y in enumerate(np.linspace(-1 * cam.screen_ratio, 1 * cam.screen_ratio, cam.y_res)):
        for screen_x, world_x in enumerate(np.linspace(-1, 1, cam.x_res)):
            col = Vec3(0,0,0)
            
            # shoot multiple rays within pixel
            for i in range(num_rays):
                if num_rays > 1:
                    ray_x = world_x + rnd.uniform(0,1) * cam.x_step
                    ray_y = world_y + rnd.uniform(0,1) * cam.y_step
                else:
                    ray_x = world_x
                    ray_y = world_y

                # shoot ray through pixel
                ray = Ray(Vec3(0,0,0), Vec3(ray_x, ray_y, -1))

                col += ray.trace(scene)

            # calculate the average pixel color
            col /= num_rays
            pixel_array[cam.y_res - 1 - screen_y][screen_x] = col.get_rgb()
    return pixel_array

def main():
    total_start = time.time()

    # set resolution and create pixel array
    camera = Camera(400, 200)

    for i, angle in enumerate(np.linspace(0,math.pi*4,12)):
        start_time = time.time()

        red_x = math.cos(angle)
        red_z = math.sin(angle) - 1.5

        # create a scene
        scene = Scene()
        scene.add_light(Light(Vec3(1,.5,-1)))
        scene.add_scene_object(Sphere(Vec3(0,-4.3,-2), 4)) # blue sphere
        scene.add_scene_object(Sphere(Vec3(0,-.25,-2), 0.5, Vec3(0,1,0), reflect=True)) # green sphere
        scene.add_scene_object(Sphere(Vec3(-1,0,-2), 0.5, Vec3(1,1,0))) # yellow sphere
        # scene.add_scene_object(Sphere(Vec3(.75,0,-2), 0.3, Vec3(1,0,0))) # red sphere
        scene.add_scene_object(Sphere(Vec3(red_x,0,red_z), 0.3, Vec3(1,0,0), reflect=True)) # red sphere

        # save final image
        image = Image.fromarray(render(scene, camera, num_rays=1))
        image.save(f"imgs/test{i:03}.png")

        print(f"Frame {i} done in {time.time() - start_time:.3f} seconds")

    print(f"Render completed in {time.time() - total_start:.3f} seconds!")

if __name__ == "__main__":
    main()