import math

def hit_sphere(ray, sphere, t_min=0, t_max=50):
    oc = ray.origin - sphere.center
    a = ray.direction.dot(ray.direction)
    b = 2 * oc.dot(ray.direction)
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

# def hit_plane(ray, plane):
#     denominator = plane.normal.dot(ray.direction)
#     if abs(denominator) > 0.0001:
#         t = (plane.center - ray.origin).dot(plane.normal) / denominator

#         if t > 0.0001:
#             return t
#     return None