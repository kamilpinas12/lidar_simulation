import numpy as np
import cv2
from keyboard import is_pressed

from simulation import Object, Simulation, show_lidar_data


object = Object(100, 100, move_noise_std=0.1, rotation_noise_std=0.04, offset=0.01, size=8)
sim = Simulation('maps/map.png', num_measurements=500, lidar_std=0,object=object)
window_name = "Lidar Simulation"


while not is_pressed('q'):
    cv2.imshow(window_name, sim.get_img())

    if is_pressed('w'):
        object.move(5)
    if is_pressed("s"):
        object.move(-5)
    if is_pressed('a'):
        object.rotate(0.1)
    if is_pressed('d'):
        object.rotate(-0.1)

    if is_pressed('g'):
        lst = sim.get_lidar_data()
        show_lidar_data(lst)


    cv2.waitKey(10)



cv2.destroyAllWindows()






