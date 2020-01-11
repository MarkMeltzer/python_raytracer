import random as rnd
import numpy as np
from PIL import Image
from classes import *
from helpers import *

def hit_sphere(ray, sphere):
    oc = ray.origin - sphere.center
    a = ray.direction.dot(ray.direction)
    b = 2 * oc.dot(ray.direction)
    c = oc.dot(oc) - sphere.radius * sphere.radius
    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        t = (-b - math.sqrt(discriminant) / (2 * a))

        # make sure we don't draw stuff behind us
        if t < 0:
            return None
        else:
            return t
    else:
        return None

def hit_plane(ray, plane):
    denominator = plane.normal.dot(ray.direction)
    if abs(denominator) > 0.0001:
        t = (plane.center - ray.origin).dot(plane.normal) / denominator

        if t > 0.0001:
            return t
    return None

def color(ray):
    unit_dir = ray.direction.get_unit()
    t = unit_dir.y + 1
    color_vector = Vec3(1,1,1) * (1 - t) + Vec3(0.5,0.7,1.0) * t
    return color_vector.get_rgb()

def main():
    # set resolution and create pixel array
    x_res = 500
    y_res = 250
    screen_ratio = y_res / x_res
    img_array = np.zeros((y_res,x_res,3), dtype=np.uint8)

    # create a scene
    scene = Scene()
    scene.add_light(Light(Vec3(1.5,1.5,0)))
    scene.add_scene_object(Sphere(Vec3(0,0,-2), 0.5))
    scene.add_scene_object(Sphere(Vec3(.5,.5,-1.5), 0.3))

    # iterate over all pixels
    for screen_y, world_y in enumerate(np.linspace(-1 * screen_ratio, 1 * screen_ratio, y_res)):
        for screen_x, world_x in enumerate(np.linspace(-1, 1, x_res)):
            # shoot ray through pixel
            ray = Ray(Vec3(0,0,0), Vec3(world_x, world_y, -1))

            # check for hits and get hits with lowest ray parameter
            min_t = np.inf
            min_object = None
            for scene_object in scene.scene_objects:
                t = hit_sphere(ray, scene_object)

                if t and t < min_t:
                    min_t = t
                    min_object = scene_object

            # if there was a hit draw it, else draw background
            if min_object:
                col = distance_to_greyscale(min_t, 3,5)
            else:
                col = color(ray)
            img_array[y_res - 1 - screen_y][screen_x] = col

    # save final image
    image = Image.fromarray(img_array)
    image.save(f"test.png")


if __name__ == "__main__":
    main()