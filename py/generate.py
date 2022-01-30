import numpy as np


def generate_data(points_size, range_x=10, range_y=10):
    x = np.random.randint(0, range_x, points_size)
    y = np.random.randint(0, range_y, points_size)

    with open("dataset/input.csv", "w") as f:
        f.write("x;y\n")
        for i in range(len(x)):
            f.write(f"{x[i]};{y[i]}\n")


generate_data(100, 1000, 1000)