from math import cos, sin, pi

def points_on_circle(no_of_points, radius, x_center, y_center):
    
    # no_of_points - number of points to be distributed on a circle
    # radius - distance from the center of the circle
    # x_center, y_center - coordinates of the center of the circle
    
    center = [x_center,y_center]
    angle = (2*pi) / no_of_points
    
    x_list = []
    y_list = []
    
    for i in range(no_of_points):
        x_list.append(center[0] + (radius * cos(angle)))
        y_list.append(center[1] + (radius * sin(angle)))
        angle = angle + ((2*pi) / no_of_points)

    return x_list, y_list

# test
# import matplotlib.pyplot as plt

# a = points_on_circle(15, 10, 20, 10)
# plt.figure(figsize=(6, 6))
# plt.scatter(a[0], a[1])
# plt.show()