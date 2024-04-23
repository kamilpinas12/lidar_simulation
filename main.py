import numpy as np
import cv2
from keyboard import is_pressed

from simulation import Object, Simulation, show_lidar_data


object = Object(100, 100, size=8)
sim = Simulation('maps/map.png', num_measurements=1000, std=0, object=object)
window_name = "Lidar Simulation"


while not is_pressed('q'):
    cv2.imshow(window_name, sim.get_img())

    if is_pressed('w'):
        sim.move(0, 5, 0)
    if is_pressed("s"):
        sim.move(0, -5, 0)
    if is_pressed('a'):
        sim.move(-5, 0, 0)
    if is_pressed('d'):
        sim.move(5, 0, 0)

    #rotate left
    if is_pressed('r'):
        sim.move(0, 0, 0.1)
    #rotate right
    if is_pressed('t'):
        sim.move(0, 0, -0.1)

    if is_pressed('g'):
        lst = sim.get_lidar_data()
        show_lidar_data(lst)


    cv2.waitKey(10)



cv2.destroyAllWindows()






