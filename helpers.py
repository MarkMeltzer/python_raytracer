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

def random_color():
    return classes.Vec3(rnd.random(), rnd.random(), rnd.random())
        
def parse_obj(filename):
    with open(filename) as f:
        lines = f.readlines()
        lines = lines[4:]

        vertices = []
        tris = []

        for line in lines:
            line = line.strip()
            line = line.split()
            if line[0] == "v":
                vertices.append(classes.Vec3(float(line[1]), float(line[2]), float(line[3])))
            elif line[0] == "f" and len(line) == 5:
                v0 = vertices[int(line[1].split("//")[0]) - 1]
                v1 = vertices[int(line[2].split("//")[0]) - 1]
                v2 = vertices[int(line[3].split("//")[0]) - 1]
                v3 = vertices[int(line[4].split("//")[0]) - 1]
                q = classes.Quad(v0,v1,v2,v3)
                t1, t2 = q.get_triangles()
                tris.append(t1)
                tris.append(t2)

    
    return tris