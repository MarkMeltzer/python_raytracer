import math
import numpy as np

x_res = 13
y_res = 3
screen_ratio = y_res / x_res
for screen_y, world_y in enumerate(np.linspace(-1 * screen_ratio, 1 * screen_ratio, y_res)):
    for screen_x, world_x in enumerate(np.linspace(-1, 1, x_res)):
        print(f"world_x: {world_x:.3f}, world_y: {world_y:.3f}")

x_step = 2 / (x_res - 1)
y_step = (2 * screen_ratio) / (y_res - 1)
print(f"x_step: {x_step:.3f}")
print(f"y_step: {y_step:.3f}")

# use "x/y_step * randfloat(0,1)" to get random point in pixel for averaging.


# for angle in np.linspace(0,math.pi*2,5):
#     x = math.cos(angle)
#     z = math.sin(angle) - 1.5

#     print(f"x:{x:.2f}, z:{z:.2f}")