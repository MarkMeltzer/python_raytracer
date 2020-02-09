import math
import numpy as np
from classes import *

with open("lowpolytree.obj") as f:
    lines = f.readlines()
    lines = lines[4:]

    vertices = []
    tris = []

    for line in lines:
        line = line.strip()
        line = line.split()
        if line[0] == "v":
            vertices.append(Vec3(float(line[1]), float(line[2]), float(line[3])))
        elif line[0] == "f":
            v0 = vertices[int(line[1].split("//")[0]) - 1]
            v1 = vertices[int(line[2].split("//")[0]) - 1]
            v2 = vertices[int(line[3].split("//")[0]) - 1]
            v3 = vertices[int(line[4].split("//")[0]) - 1]
            q = Quad(v0,v1,v2,v3)
            t1, t2 = q.get_triangles()
            tris.append(t1)
            tris.append(t2)
print(len(tris))



# v1 = Vec3(1,2,3)
# v2 = Vec3(4,5,6)
# l = [v1,v2]
# print(sum(l))


# x_res = 13
# y_res = 3
# screen_ratio = y_res / x_res
# for screen_y, world_y in enumerate(np.linspace(-1 * screen_ratio, 1 * screen_ratio, y_res)):
#     for screen_x, world_x in enumerate(np.linspace(-1, 1, x_res)):
#         print(f"world_x: {world_x:.3f}, world_y: {world_y:.3f}")

# x_step = 2 / (x_res - 1)
# y_step = (2 * screen_ratio) / (y_res - 1)
# print(f"x_step: {x_step:.3f}")
# print(f"y_step: {y_step:.3f}")

# use "x/y_step * randfloat(0,1)" to get random point in pixel for averaging.


# for angle in np.linspace(0,math.pi*2,10):
#     x = math.cos(-angle)
#     z = math.sin(-angle) - 1.5

#     print(f"x:{x:.2f}, z:{z:.2f}")