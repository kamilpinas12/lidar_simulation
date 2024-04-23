import numpy as np
import cv2
from simulation.object import Object

class Simulation():
    def __init__(self, img_path:str, num_measurements:int, std:float, object: object):
        '''
        :param str num_measuremetn: number of measurement per one rotation
        :param float std: standard deviation of noise in data
        '''
        self.object = object
        self.num_measurements = num_measurements
        self.std = std
        self.object = object

        self.img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)


    def move(self, delta_x: float, delta_y: float, delta_angle:float):
        self.object.x_pos += delta_x
        self.object.y_pos += delta_y
        self.object.angle += delta_angle


    def get_lidar_data(self):
        lst = np.zeros((self.num_measurements, 2))
        lst[:, 0] = np.linspace(0, np.pi*2, self.num_measurements, endpoint=False)
        position = np.array([self.object.x_pos, self.object.y_pos])
        for i in range(self.num_measurements):
            angle = self.object.angle + lst[i, 0]
            v = np.array([np.cos(angle), np.sin(angle)])
            v_sum = v + position
            num_iter = 1
            while 0 < round(v_sum[0]) < self.img.shape[1] and 0 < round(v_sum[1]) < self.img.shape[0]:
                idx = np.round(v_sum).astype(int)
                if self.img[self.img.shape[0]-idx[1], idx[0]] == 0:
                    break
                v_sum += v
                num_iter += 1
            v = v*num_iter
            lst[i, 1] = np.sqrt(v[0]**2 + v[1]**2) 

        noise = self.std * np.random.randn(self.num_measurements)
        lst[:, 1] += noise
        return lst


    def get_img(self):
        return self.object.add_object_to_img(self.img)





