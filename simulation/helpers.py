import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import os
import time
from typing import List


matplotlib.use('agg')

if not os.path.exists("data"):
    os.makedirs("data")


def show_lidar_data(data: np.ndarray, overwrite_file: bool=False):
    x = np.cos(data[:, 0] + np.pi/2)*data[:, 1]
    y = np.sin(data[:, 0] + np.pi/2)*data[:, 1]
    
    plt.figure()
    plt.scatter(x, y)
    plt.scatter([0], [0])

    plt.title("Lidar data visualization")
    plt.grid()
    plt.axis('scaled')
    if overwrite_file:
        plt.savefig('data/lidar_data.png')
    else:
        plt.savefig(f"data/lidar_data {time.ctime(time.time())}.png")


def show_map(data: List[List]):
    x = []
    y = []    
    for i in data:
        x.append(i[0])
        y.append(i[1])

    plt.figure()
    plt.scatter(x, y)
    plt.grid()
    plt.axis('scaled')
    plt.savefig('data/map.png')
    plt.figure()



def polar2kart(lidar_data: np.ndarray):
    x = np.round(np.cos(lidar_data[:, 0])*lidar_data[:, 1])
    y = np.round(np.sin(lidar_data[:, 0])*lidar_data[:, 1])
    lst = np.zeros((x.size, 2))
    lst[:, 0], lst[:, 1] = x, y
    return lst


def kart2polar(data: np.ndarray):
    data_polar = np.zeros(data.shape)
    for i in range(data.shape[0]):
        d = np.linalg.norm(data[i, :])
        data_polar[i, 1] = d

        angle = np.arctan2(data[i, 0], data[i, 1])
        if angle < 0:
            angle = np.pi -angle
        data_polar[i, 0] = angle

    return data_polar
