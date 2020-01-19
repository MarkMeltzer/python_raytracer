import random as rnd
import numpy as np
from PIL import Image
import math
from classes import *
from helpers import *

def hit_sphere(ray, sphere, t_min=0, t_max=50):
    oc = ray.origin - sphere.center
    a = ray.direction.dot(ray.direction)
    b = 2 * oc.dot(ray.direction)
    c = oc.dot(oc) - sphere.radius * sphere.radius
    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        t = (-b - math.sqrt(discriminant) / (2 * a))

        # make sure we don't draw stuff behind us
        if t < t_min or t > t_max:
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

def render(scene, cam=Camera(200, 100)):
    pixel_array = cam.get_pixel_array()

    # iterate over all pixels
    for screen_y, world_y in enumerate(np.linspace(-1 * cam.screen_ratio, 1 * cam.screen_ratio, cam.y_res)):
        for screen_x, world_x in enumerate(np.linspace(-1, 1, cam.x_res)):
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
                # trace a ray from hitpoint towards the light
                shadow_origin = ray.get_point(min_t)
                shadow_direction = scene.lights[0].position - shadow_origin
                shadow_ray = Ray(shadow_origin, shadow_direction)

                # check for shadow
                in_shadow = False
                for scene_object in scene.scene_objects:
                    if hit_sphere(shadow_ray, scene_object) and scene_object is not min_object:
                        in_shadow = True
                        shadow_object = scene_object
                        break

                if in_shadow:
                    col = shadow_object.color_vector.get_rgb()
                else:
                    col = distance_to_greyscale(min_t, min_value=1, max_value=10)
                    # col = min_object.color_vector.get_rgb()
            elif hit_sphere(ray, scene.lights[0].render_sphere):
                # draw the light
                col = Vec3(1,1,0).get_rgb()
            else:
                # draw the background
                col = color(ray)
            pixel_array[cam.y_res - 1 - screen_y][screen_x] = col
    return pixel_array

def main():
    # set resolution and create pixel array
    camera = Camera(200, 100)

    for i, angle in enumerate(np.linspace(0,math.pi*2,240)):
        red_x = math.cos(angle)
        red_z = math.sin(angle) - 1.5

        # create a scene
        scene = Scene()
        scene.add_light(Light(Vec3(.75,.5,-2)))
        scene.add_scene_object(Sphere(Vec3(0,-4.3,-2), 4)) # blue sphere
        scene.add_scene_object(Sphere(Vec3(0,0,-2), 0.5, Vec3(0,1,0))) # green sphere
        scene.add_scene_object(Sphere(Vec3(red_x,.5,red_z), 0.3, Vec3(1,0,0))) # red sphere

        # save final image
        image = Image.fromarray(render(scene, camera))
        image.save(f"imgs/test{i:03}.png")

        print(f"i:{i}, x:{red_x}, z:{red_z}")


if __name__ == "__main__":
    main()