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
        self.phong = settings["phong"]

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
        hit_result = self.get_intersection(self.scene.scene_objects, ray)

        # if there was a hit draw it, else draw background
        if hit_result:
            col = hit_result[1].color_vector
            hit_point = ray.get_point(hit_result[0])
            hit_normal = hit_result[1].get_normal(hit_point)
            new_ray_origin = hit_point + hit_normal * 0.001
            light = self.scene.lights[0]
            
            # reflection
            if self.reflection and hit_result[1].mat.reflect:
                reflect_ray = self.get_reflected_ray(new_ray_origin, ray.direction, hit_normal)
                reflect_col = self.trace(reflect_ray, num_bounces=num_bounces)
                col = reflect_col * hit_result[1].mat.reflect + col * (1 - hit_result[1].mat.reflect)
            
            # hard shadows
            if self.hard_shadows:
                if self.get_hard_shadow(new_ray_origin, light):
                    col *= 0.2
            
            # lambert shading
            diffuse = 0
            if self.lambert or self.phong:
                diffuse = self.get_lambert_shading(hit_normal, (light.position - new_ray_origin), hit_result[1].mat.albedo)
                diffuse = col * diffuse

            # specular shading
            specular = 0
            if self.phong:
                reflect = self.get_reflected_ray(new_ray_origin, (light.position - new_ray_origin).get_unit(), hit_normal)
                specular = max(0, ray.direction.dot(reflect.direction))**500
                specular = Vec3(1,1,1) * specular

            # return color of object
            if self.lambert:
                col = diffuse

            if self.phong:
                Ks = hit_result[1].mat.Ks
                Kd = hit_result[1].mat.Kd
                Ka = self.scene.Ka
                col = Vec3(1,1,1) * Ka + diffuse * Kd + specular * Ks
            
            return col.clip(0,1)
        # elif ray.hit_sphere(self.scene.lights[0].render_sphere):
        #     # draw the light
        #     return Vec3(1,1,0)
        else:
            # draw the background
            return helpers.color(ray)

    def get_hard_shadow(self, shadow_origin, light):
        shadow_direction = (light.position - shadow_origin).get_unit()
        shadow_ray = Ray(shadow_origin, shadow_direction)
        shadow_result = self.get_intersection(self.scene.scene_objects, shadow_ray, any_hit=True)

        if shadow_result:
            return Vec3(0,0,0)
        return None

    def get_reflected_ray(self, reflect_origin, incident_direction, hit_normal):
        reflect_direction = incident_direction - hit_normal * 2 * hit_normal.dot(incident_direction)
        return Ray(reflect_origin, reflect_direction)

    def get_lambert_shading(self, normal, light_ray, albedo):
        return albedo * max(0, normal.dot(light_ray.get_unit()))

    def get_intersection(self, scene_objects, ray, any_hit=False):
        # find the hit object with the smallest parameter
        min_t = np.inf
        min_object = None
        for scene_object in scene_objects:
            t = scene_object.get_hit(ray)

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

    def clip(self, min_val, max_val):
        x = max(min_val, self.x)
        x = min(max_val, self.x)

        y = max(min_val, self.y)
        y = min(max_val, self.y)

        z = max(min_val, self.z)
        z = min(max_val, self.z)

        return Vec3(x,y,z)

    def crossproduct(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x  * other.z
        z = self.x * other.y - self.y * other.x
        return Vec3(x,y,z)

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


class Material():
    def __init__(self, albedo=0.8, Kd=1, Ks=.5, n=500, reflect=0):
        self.albedo = albedo    # general factor of light reflected
        self.Kd = Kd            # specular parameter, [0-1], "diffuseness"
        self.Ks = Ks            # specular parameter, [0-1], "glossyness"
        self.n = n              # specular highlight size, n > 0 
        self.reflect = reflect  # reflectiveness, [0-1], factor of how mirror-like a surface is

class Sphere():
    def __init__(self, center, radius, color_vector=Vec3(0,0,1), mat=Material()):
        self.center = center
        self.radius = radius
        self.color_vector = color_vector
        self.mat = mat

    def get_normal(self, point):
        normal = (point - self.center).get_unit()
        return normal

    def get_hit(self, ray, t_min=0, t_max=50):
        # notes:
        # a = ray.direction dot ray.direction, since directions are unit vectors
        # a is always 1

        oc = ray.origin - self.center
        a = 1
        b = 2 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
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
        return f"sphere with color: {self.color_vector.get_rgb()}"

class Triangle():
    def __init__(self, v0, v1, v2, color_vector=Vec3(1,0,0), mat=Material()):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.color_vector = color_vector
        self.mat = mat
        self.normal = self.calculate_normal()

    def calculate_normal(self):
        a = self.v1 - self.v0
        b = self.v2 - self.v0
        N = a.crossproduct(b)
        return N

    def get_normal(self, _):
        return self.normal

    def get_hit(self, ray):
        # source: https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
        ### get normal ###
        N = self.normal

        ### check intersection with plane ###
        NdotDir = N.dot(ray.direction)

        if abs(NdotDir) < 0.001:
            # plane is parallel to ray, not intersection
            return None

        D = N.dot(self.v0)
        t = (N.dot(ray.origin) + D) / NdotDir
        
        if t < 0:
            # ray is behind camera
            return None

        P = ray.origin + ray.direction * t

        ### check if p is in triangle using inside out test ###
        # edge 0
        edge0 = self.v1 - self.v0
        C = edge0.crossproduct(P - self.v0)
        if N.dot(C) < 0:
            # P is on the right side of the edge, so outside of the triangle
            return None

        # edge 1
        edge1 = self.v2 - self.v1
        C = edge1.crossproduct(P - self.v1)
        if N.dot(C) < 0:
            # P is on the right side of the edge, so outside of the triangle
            return None

        # edge 2
        edge2 = self.v0 - self.v2
        C = edge2.crossproduct(P - self.v2)
        if N.dot(C) < 0:
            # P is on the right side of the edge, so outside of the triangle
            return None

        return t
    
    def translate_x(self, dist):
        self.v0.x += dist
        self.v1.x += dist
        self.v2.x += dist
    
    def translate_y(self, dist):
        self.v0.y += dist
        self.v1.y += dist
        self.v2.y += dist

    def translate_z(self, dist):
        self.v0.z += dist
        self.v1.z += dist
        self.v2.z += dist

    def translate(self, x_dist=0, y_dist=0, z_dist=0):
        self.translate_x(x_dist)
        self.translate_y(y_dist)
        self.translate_z(z_dist)

    def __str__(self):
        return f"triangle with vertices: {self.v0}, {self.v1} and {self.v2}"


class Plane():
    def __init__(self, center, normal):
        self.center = center
        self.normal = normal.get_unit()

class Scene():
    def __init__(self, Ka=0.1):
        self.lights = []
        self.scene_objects = []
        self.Ka = Ka        # ambient light factor

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
