from classes import *

def distance_to_greyscale(value, min_value=0, max_max=100):
    value = (value - min_value) / (max_max - min_value)
    color_vector = Vec3(1,1,1) * (1 - value) + Vec3(0,0,0) * value
    return color_vector.get_rgb()
