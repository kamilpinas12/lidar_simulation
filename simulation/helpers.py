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


def show_map(data: List[List], occupancy_map: np.ndarray):
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
    plt.close()
    
    plt.figure()
    plt.imshow(occupancy_map*256, cmap='gray', vmin=0, vmax=256)
    plt.axis('off')
    plt.xlabel('x')
    plt.savefig('data/occupancy_map.png')
    plt.close()



def polar2kart(lidar_data: np.ndarray):
    x = np.round(np.cos(lidar_data[:, 0])*lidar_data[:, 1])
    y = np.round(np.sin(lidar_data[:, 0])*lidar_data[:, 1])
    lst = np.zeros((x.size, 2))
    lst[:, 0], lst[:, 1] = x, y
    return lst

