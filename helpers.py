import classes
import random as rnd

def distance_to_greyscale(value, min_value=0, max_value=100):
    value = (value - min_value) / (max_value - min_value)
    color_vector = classes.Vec3(1,1,1) * (1 - value) + classes.Vec3(0,0,0) * value
    return color_vector

def color(ray):
    unit_dir = ray.direction.get_unit()
    t = unit_dir.y + 1
    color_vector = classes.Vec3(1,1,1) * (1 - t) + classes.Vec3(0.5,0.7,1.0) * t
    return color_vector

def random_point():
    point = classes.Vec3(9999,9999,9999)
    while point.get_squared() >= 1:
        point = classes.Vec3(rnd.uniform(-1,1),rnd.uniform(-1,1),rnd.uniform(-1,1))
    return point