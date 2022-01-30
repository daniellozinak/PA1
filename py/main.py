import math
import threading as t
import time

import numpy as np


class CustomThread(t.Thread):
    def __init__(self, clusters, n_points):
        t.Thread.__init__(self)
        self.clusters = clusters
        self.n_points = n_points

    def run(self):
        self.n_points = assign_cluster(self.clusters, self.n_points)


def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


def mean(points):
    x = 0
    y = 0
    for point in points:
        x += point[0]
        y += point[1]
    return [x / len(points), y / len(points)]


def write_to_file(result):
    with open("dataset/result.csv", "w") as f:
        for i in range(len(result)):
            for j in range(len(result[i])):
                if j != 0:
                    f.write(f"{float(result[i][j][0])} {float(result[i][j][1])};{result[i][0][0]} {result[i][0][1]}\n")


def assign_cluster(clusters, points):
    result_points = points.tolist().copy()
    for point in result_points:
        chosen_index = 0
        for i in range(len(clusters)):
            distance_close = distance(clusters[chosen_index], point)
            distance_current = distance(clusters[i], point)
            if distance_close > distance_current:
                chosen_index = i
        if len(point) < 3:
            point.append(chosen_index)
        else:
            point[2] = chosen_index
    return result_points


def assing_cluster_single(clusters, points):
    for point in points:
        chosen_index = 0
        for i in range(len(clusters)):
            distance_close = distance(clusters[chosen_index], point)
            distance_current = distance(clusters[i], point)
            if distance_close > distance_current:
                chosen_index = i
        if len(point) < 3:
            point.append(chosen_index)
        else:
            point[2] = chosen_index


def k_means_thread(data, k):
    clusters = []
    for i in range(k):
        clusters.append(data[i].copy())

    change = True
    while change:
        # assign points to center points
        split = np.array_split(data, k)
        threads = []
        for i in range(k):
            temp_thread = CustomThread(clusters, split[i])
            temp_thread.start()
            threads.append(temp_thread)

        data = []
        for t in threads:
            t.join()
            for point in t.n_points:
                data.append(point)

        change = False
        # recalculate clusters
        for i in range(len(clusters)):
            temp = []
            for point in data:
                if point[2] == i:
                    temp.append(point)
            if len(temp) > 0:
                avg = mean(temp)
                if avg != clusters[i]:
                    change = True
                clusters[i] = avg
    return data, clusters


def k_means_single(data, k):
    clusters = []
    for i in range(k):
        clusters.append(data[i].copy())

    change = True
    while change:
        # assign points to center points
        assing_cluster_single(clusters, data)

        change = False
        # recalculate clusters
        for i in range(len(clusters)):
            temp = []
            for point in data:
                if point[2] == i:
                    temp.append(point)
            if len(temp) > 0:
                avg = mean(temp)
                if avg != clusters[i]:
                    change = True
                clusters[i] = avg
    return data, clusters


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            try:
                point = line.replace("\n", "").split(";")
                data.append([int(point[0]), int(point[1])])
                pass
            except:
                continue

    return data


def run(k):
    print("reading data")
    data = read_data("dataset/input.csv")
    res = k_means_thread(data, k)
    points = res[0]
    clusters = res[1]

    with open("dataset/result_points.csv", "w") as f:
        print("writing data in result_points.csv")
        f.write("x;y;cluster_index\n")
        for point in points:
            f.write(f"{point[0]};{point[1]};{point[2]}\n")
    with open("dataset/result_clusters.csv", "w") as f:
        print("writing clusters in result_clusters.csv")
        f.write("x:y\n")
        for cluster in clusters:
            f.write(f"{cluster[0]};{cluster[1]}\n")


run(8)