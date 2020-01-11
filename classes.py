import math

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
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

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if type(other) == Vec3:
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __str__(self):
        return str(self.get_tuple())

class Sphere():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

class Plane():
    def __init__(self, center, normal):
        self.center = center
        self.normal = normal.get_unit()

class Scene():
    def __init__(self, lights=[], scene_objects=[]):
        self.lights = lights
        self.scene_objects = scene_objects

    def add_scene_object(self, scene_object):
        self.scene_objects.append(scene_object)

    def add_light(self, light):
        self.lights.append(light)

class Light():
    def __init__(self, position):
        self.position = position