import math
import numpy as np
import helpers

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

    def trace(self, scene):
        # check for hits and get hits with lowest ray parameter
        hit_result = self.get_intersection(scene.scene_objects)

        # if there was a hit draw it, else draw background
        if hit_result:
            # trace a new ray in a random direction
            new_origin = self.get_point(hit_result[0])
            new_target = new_origin + hit_result[1].get_normal(new_origin) + helpers.random_point()
            new_direction = (new_target - new_origin).get_unit()
            new_ray = Ray(new_origin, new_direction)

            col  = new_ray.trace(scene) * 0.5
            
        # elif self.hit_sphere(scene.lights[0].render_sphere):
        #     # draw the light
        #     col = Vec3(1,1,0)
        else:
            # draw the background
            col = helpers.color(self)
        
        return col

    def hit_sphere(self, sphere, t_min=0, t_max=50):
        oc = self.origin - sphere.center
        a = self.direction.dot(self.direction)
        b = 2 * oc.dot(self.direction)
        c = oc.dot(oc) - sphere.radius * sphere.radius
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            t1 = (-b - math.sqrt(discriminant) / (2 * a))
            t2 = (-b + math.sqrt(discriminant) / (2 * a))
            t = min(t1, t2)

            # make sure we don't draw stuff behind us
            if t < t_min or t > t_max:
                return None
            else:
                return t
        else:
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
    def __init__(self, center, radius, color_vector=Vec3(0,0,1)):
        self.center = center
        self.radius = radius
        self.color_vector = color_vector

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