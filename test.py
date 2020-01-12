import math
import numpy as np

for angle in np.linspace(0,math.pi*2,5):
    x = math.cos(angle)
    z = math.sin(angle) - 1.5

    print(f"x:{x:.2f}, z:{z:.2f}")