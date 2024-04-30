import numpy as np
import cv2
from simulation import Object


class Simulation():
    def __init__(self, img_path:str, num_measurements:int, distance_std:float, angle_std: float, lidar_range: float, object: object):
        '''
        :param str num_measuremetn: number of measurement per one rotation
        '''
        self.num_measurements = num_measurements
        self.distance_std = distance_std
        self.angle_std = angle_std
        self.lidar_range = lidar_range

        self.object = object
        self.map = []
        self.img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        self.window_name = "Lidar Simulation"


    def get_lidar_data(self) -> np.ndarray:
        lst = np.zeros((self.num_measurements, 2))
        lst[:, 0] = np.linspace(0, np.pi*2, self.num_measurements, endpoint=False)
        position = np.array([self.object.real_x_pos, self.object.real_y_pos])
        for i in range(self.num_measurements):
            angle = self.object.real_angle + lst[i, 0]
            noise = np.random.randn(2) * self.angle_std
            v = np.array([np.cos(angle + noise[0]), np.sin(angle + noise[1])])
            v_sum = v + position
            num_iter = 1
            while 0 < round(v_sum[0]) < self.img.shape[1] and 0 < round(v_sum[1]) < self.img.shape[0]:
                if self.lidar_range and num_iter >= self.lidar_range:
                    break
                idx = np.round(v_sum).astype(int)
                if self.img[self.img.shape[0]-idx[1], idx[0]] == 0:
                    break
                v_sum += v
                num_iter += 1
            if self.lidar_range and num_iter >= self.lidar_range:
                lst[i, 1] = None
            else:
                v = v*num_iter
                lst[i, 1] = np.sqrt(v[0]**2 + v[1]**2) + np.random.randn(1)[0] * self.distance_std 

        return lst


    def get_img(self, show_theoretical_position: bool=False) -> np.ndarray:
        if show_theoretical_position:
            pos = self.object.get_position()
            obj = Object(x_pos=pos[0], y_pos=pos[1], angle=pos[2], size=self.object.size, color1=210, color2=160)
            img = obj.add_object_to_img(self.img)
            return self.object.add_object_to_img(img)
        else:
            return self.object.add_object_to_img(self.img)


    def update_map(self, lidar_data: np.ndarray, x_pos:float, y_pos:float, angle:float):
        x = np.round(np.cos(lidar_data[:, 0] + angle)*lidar_data[:, 1] + x_pos)
        y = np.round(np.sin(lidar_data[:, 0] + angle)*lidar_data[:, 1] + y_pos)
        
        for i in range(x.shape[0]):
            tab = [x[i], y[i]]
            if tab not in self.map:
                self.map.append(tab)



    def clear_map(self):
        self.map = []


    def update(self, show_theoretical_position: bool=False):
        cv2.imshow(self.window_name, self.get_img(show_theoretical_position))
        cv2.waitKey(10)


    def end_sim(self):
        cv2.destroyAllWindows()