import random
import numpy as np
import matplotlib.pyplot as plt


def read_clusters(filename):
    data = []
    with open(filename) as f:
        for line in f:
            try:
                temp = line.replace("\n", "").split(";")
                data.append([float(temp[0]), float(temp[1])])
            except:
                continue
    return data


def read_points(filename):
    data = []
    with open(filename) as f:
        for line in f:
            try:
                temp = line.replace("\n", "").split(";")
                data.append([int(temp[0]), int(temp[1]), int(temp[2])])
            except:
                continue
    return data


def run(points, clusters):
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(len(clusters))]

    for i in range(len(clusters)):
        center_x = clusters[i][0]
        center_y = clusters[i][1]
        x_cors = []
        y_cors = []
        for point in points:
            if point[2] == i:
                x_cors.append(point[0])
                y_cors.append(point[1])
        # print(f"{i} -> {np.array(x_cors)} {np.array(y_cors)}")
        plt.scatter(np.array(x_cors), np.array(y_cors), c=color[i])
        plt.scatter([center_x], [center_y], c=color[i], s=200, alpha=0.3)

    plt.show()

run(read_points("dataset/result_points.csv"), read_clusters("dataset/result_clusters.csv"))