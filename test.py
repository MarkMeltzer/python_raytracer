import math
import numpy as np

x_res = 4
y_res = 2
screen_ratio = y_res / x_res
for screen_y, world_y in enumerate(np.linspace(-1 * screen_ratio, 1 * screen_ratio, y_res)):
    for screen_x, world_x in enumerate(np.linspace(-1, 1, x_res)):
        print(f"world_x: {world_x:.3f}, world_y: {world_y:.3f}")


# for angle in np.linspace(0,math.pi*2,5):
#     x = math.cos(angle)
#     z = math.sin(angle) - 1.5

#     print(f"x:{x:.2f}, z:{z:.2f}")