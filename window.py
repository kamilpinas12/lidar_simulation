import numpy as np
import cv2
from pynput import keyboard

from simulation import Object, Simulation, show_lidar_data

class Window:
    def __init__(self):
        self.working = True
        self.object = Object(100, 100, size=8)
        self.sim = Simulation('maps/map.png', num_measurements=500, std=0, object=self.object)
        self.window_name = "Lidar Simulation"  
        self.listener = keyboard.Listener(on_press=self.on_press)      
        
    def run(self):
        self.listener.start()
        while self.working:
            self.update()
        cv2.destroyAllWindows()
            
    def update(self):
        cv2.imshow(self.window_name, self.sim.get_img())
        cv2.waitKey(10)
    
    def on_press(self, key):
        if key.char == 'w':
            self.sim.move(0, 5, 0)
        if key.char == 's':
            self.sim.move(0, -5, 0)
        if key.char == 'a':
            self.sim.move(-5, 0, 0)
        if key.char == 'd':
            self.sim.move(5, 0, 0)
        if key.char == 'r':
            self.sim.move(0, 0, 0.1)
        if key.char == 't':
            self.sim.move(0, 0, -0.1)
        if key.char == 'g':
            lst = self.sim.get_lidar_data()
            show_lidar_data(lst)
        if key.char == 'q':
            self.working = False
        
    