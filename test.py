from simulation import Simulation, Object, ICP
import simulation
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time

matplotlib.use('TkAgg')

o = Object(100, 100, move_noise_std=0, rotation_noise_std=0, angle=0)
sim = Simulation("maps/map.png", num_measurements=100, distance_std=0, angle_std=0, lidar_range=600, object=o)
lidar_data = sim.get_lidar_data()

x = np.round(np.cos(lidar_data[:, 0] + o.angle)*lidar_data[:, 1] + o.x)
y = np.round(np.sin(lidar_data[:, 0] + o.angle)*lidar_data[:, 1] + o.y)
o.rotate(np.pi/24)
o.move(9)

lidar_data = sim.get_lidar_data()
x1 = np.round(np.cos(lidar_data[:, 0])*lidar_data[:, 1] + o.x)
y1 = np.round(np.sin(lidar_data[:, 0])*lidar_data[:, 1] + o.y)

t0 = [[x,y] for x, y in zip(x, y)]
t1 = [[x,y] for x, y in zip(x1, y1)]

m = np.array(t0)
d = np.array(t1)
a = ICP(m, d)
t = time.time()
a.iterate(10)
print(f"{time.time() - t}s")
data = a.get_transformed_data()



plt.plot(data[:, 0], data[:, 1],".r", label="ICP 10 iterations")
plt.plot(x1, y1, ".g", label="Lidar data")
plt.plot(x, y, ".b", label="map")
plt.legend()
plt.show()
