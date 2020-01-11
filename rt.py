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
        return (-b - math.sqrt(discriminant) / (2 * a))
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
    x_res = 1280
    y_res = 720
    screen_ratio = y_res / x_res

    img_array = np.zeros((y_res,x_res,3), dtype=np.uint8)

    # iterate over all pixels
    for screen_y, world_y in enumerate(np.linspace(-1 * screen_ratio, 1 * screen_ratio, y_res)):
        for screen_x, world_x in enumerate(np.linspace(-1, 1, x_res)):
            ray = Ray(Vec3(0,0,0), Vec3(world_x, world_y, -1))
            sphere = Sphere(Vec3(0,0,-2), 0.5)
            plane = Plane(Vec3(0,-1,-2), Vec3(0,1,0))

            t = hit_sphere(ray, sphere)
            t2 = hit_plane(ray, plane)
            
            col = color(ray)

            if t2:
                col = distance_to_greyscale(t2, 0, 25)
            
            if t:
                col = distance_to_greyscale(t, 0, 5.5)
                
                        
            img_array[y_res - 1 - screen_y][screen_x] = col

    image = Image.fromarray(img_array)
    image.save(f"test.png")


if __name__ == "__main__":
    main()