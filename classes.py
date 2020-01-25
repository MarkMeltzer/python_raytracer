import math
import numpy as np
import helpers
import random as rnd

class Renderer():
    def __init__(self, camera, scene, settings):
        self.cam = camera
        self.scene = scene
        
        self.hard_shadows = settings["hard_shadows"]
        self.reflection = settings["reflection"]
        self.lambert = settings["lambert"]

    def render(self, num_rays=25):
        pixel_array = self.cam.get_pixel_array()

        # iterate over all pixels
        for screen_y, world_y in enumerate(np.linspace(-1 * self.cam.screen_ratio, 1 * self.cam.screen_ratio, self.cam.y_res)):
            for screen_x, world_x in enumerate(np.linspace(-1, 1, self.cam.x_res)):
                col = Vec3(0,0,0)
                
                # shoot multiple rays within pixel
                for _ in range(num_rays):
                    if num_rays > 1:
                        ray_x = world_x + rnd.uniform(0,1) * self.cam.x_step
                        ray_y = world_y + rnd.uniform(0,1) * self.cam.y_step
                    else:
                        ray_x = world_x
                        ray_y = world_y

                    # shoot ray through pixel
                    ray = Ray(Vec3(0,0,0), Vec3(ray_x, ray_y, -1))

                    col += self.trace(ray)

                # calculate the average pixel color
                col /= num_rays
                pixel_array[self.cam.y_res - 1 - screen_y][screen_x] = col.get_rgb()
        return pixel_array

    def trace(self, ray, num_bounces=0):
        num_bounces += 1
        if num_bounces > 4:
            return helpers.color(ray)

        # check for hits and get hits with lowest ray parameter
        hit_result = ray.get_intersection(self.scene.scene_objects)

        # if there was a hit draw it, else draw background
        if hit_result:
            col = hit_result[1].color_vector
            hit_point = ray.get_point(hit_result[0])
            hit_normal = hit_result[1].get_normal(hit_point)
            new_ray_origin = hit_point + hit_normal * 0.001
            light = self.scene.lights[0]
            
            # reflection
            if self.reflection and hit_result[1].reflect:
                reflect_ray = self.get_reflected_ray(new_ray_origin, ray.direction, hit_normal)
                reflect_col = self.trace(reflect_ray, num_bounces=num_bounces)
                col = reflect_col * hit_result[1].reflect + col * (1 - hit_result[1].reflect)
            
            # hard shadows
            if self.hard_shadows:
                if self.get_hard_shadow(new_ray_origin, light):
                    col /= 5
            
            # lambert shading
            if self.lambert:
                sh = self.get_lambert_shading(hit_normal, (light.position - new_ray_origin), 3)
                col *= sh

            # return color of object
            return col
        elif ray.hit_sphere(self.scene.lights[0].render_sphere):
            # draw the light
            return Vec3(1,1,0)
        else:
            # draw the background
            return helpers.color(ray)

    def get_hard_shadow(self, shadow_origin, light):
        shadow_direction = (light.position - shadow_origin).get_unit()
        shadow_ray = Ray(shadow_origin, shadow_direction)
        shadow_result = shadow_ray.get_intersection(self.scene.scene_objects, any_hit=True)

        if shadow_result:
            return Vec3(0,0,0)
        return None

    def get_reflected_ray(self, reflect_origin, incident_direction, hit_normal):
        reflect_direction = incident_direction - hit_normal * 2 * hit_normal.dot(incident_direction)
        return Ray(reflect_origin, reflect_direction)

    def get_lambert_shading(self, normal, light_ray, albedo):
        return albedo / math.pi * max(0, normal.dot(light_ray.get_unit()))


class Camera():
    def __init__(self, x_res, y_res):
        self.x_res = x_res
        self.y_res = y_res
        self.screen_ratio = self.y_res / self.x_res
        self.x_step = 2 / (x_res - 1)
        self.y_step = (2 * self.screen_ratio) / (y_res - 1)

    def get_pixel_array(self):
        return np.zeros((self.y_res,self.x_res,3), dtype=np.uint8)

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.get_unit()
    
    def get_point(self, t):
        return self.origin + self.direction * t

    def get_intersection(self, scene_objects, any_hit=False):
        # find the hit object with the smallest parameter
        min_t = np.inf
        min_object = None
        for scene_object in scene_objects:
            t = self.hit_sphere(scene_object)

            # there is a hit and its the new closest hit
            if t and t < min_t:
                min_t = t
                min_object = scene_object

                # stop early when any object is hit
                if any_hit:
                    break
        
        if min_object:
            return min_t, min_object
        else:
            return None

    def hit_sphere(self, sphere, t_min=0, t_max=50):
        # notes:
        # a = ray.direction dot ray.direction, since directions are unit vectors
        # a is always 1

        oc = self.origin - sphere.center
        a = 1
        b = 2 * oc.dot(self.direction)
        c = oc.dot(oc) - sphere.radius * sphere.radius
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            sqrt_discriminant = math.sqrt(discriminant)

            t0 = (-b - sqrt_discriminant) / 2
            t1 = (-b + sqrt_discriminant) / 2
            
            # make sure t0 is the lower t
            t0, t1 = min(t0, t1), max(t0, t1)

            # don't draw stuff behind the origin
            if t1 >= 0:
                if t0 < 0:
                    # origin is within the sphere
                    return t1 if t1 > t_min or t1 < t_max else None
                else:
                    # either single hit or hit with lowest t
                    return t0 if t0 > t_min or t0 < t_max else None

        # no hit
        return None

    def __str__(self):
        return f"o: {self.origin}, d: {self.direction}"

class Vec3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_tuple(self):
        return (self.x, self.y, self.z)
    
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def get_unit(self):
        length = self.get_length()
        return Vec3(self.x / length, self.y / length, self.z / length)

    def get_rgb(self):
        return (self.x * 255, self.y * 255, self.z * 255)

    def get_squared(self):
        return self.x**2 + self.y**2 + self.z**2
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    __radd__ = __add__

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if type(other) == Vec3:
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if type(other) == Vec3:
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vec3(self.x / other, self.y / other, self.z / other)

    def __str__(self):
        return str(self.get_tuple())

class Sphere():
    def __init__(self, center, radius, color_vector=Vec3(0,0,1), reflect=False):
        self.center = center
        self.radius = radius
        self.color_vector = color_vector
        self.reflect = reflect

    def get_normal(self, point):
        normal = (point - self.center).get_unit()
        return normal

    def __str__(self):
        return f"sphere with color: {self.color_vector.get_rgb()}"

class Plane():
    def __init__(self, center, normal):
        self.center = center
        self.normal = normal.get_unit()

class Scene():
    def __init__(self):
        self.lights = []
        self.scene_objects = []

    def add_scene_object(self, scene_object):
        self.scene_objects.append(scene_object)

    def add_light(self, light):
        self.lights.append(light)

    def __str__(self):
        return f"lights: {self.lights}, objects: {self.scene_objects}"

class Light():
    def __init__(self, position):
        self.position = position
        self.render_sphere = Sphere(position, 0.1)

class Material():
    def __init__(self, albedo=0.18):
        self.albedo = albedo