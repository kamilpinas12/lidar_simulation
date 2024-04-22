import numpy as np
import matplotlib.pyplot as plt 


def show_lidar_data(data: np.ndarray):
    x = np.cos(data[:, 0] + np.pi/2)*data[:, 1]
    y = np.sin(data[:, 0] + np.pi/2)*data[:, 1]
    
    plt.scatter(x, y)
    plt.scatter([0], [0])

    plt.title("Lidar data visualization")
    plt.grid()
    plt.axis('scaled')
    plt.show()



