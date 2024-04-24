import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import os


matplotlib.use('agg')

if not os.path.exists("data"):
    os.makedirs("data")


def show_lidar_data(data: np.ndarray):
    x = np.cos(data[:, 0] + np.pi/2)*data[:, 1]
    y = np.sin(data[:, 0] + np.pi/2)*data[:, 1]
    
    plt.figure()
    plt.scatter(x, y)
    plt.scatter([0], [0])

    plt.title("Lidar data visualization")
    plt.grid()
    plt.axis('scaled')
    plt.savefig("data/lidar_data.png")
