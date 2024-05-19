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
        self.occupancy_grid_map = OccupancyGridMap((856, 509), 1)
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
                
        self.occupancy_grid_map.occupancy_grid_mapping(lidar_data, int(x_pos), int(y_pos), angle)
        self.occupancy_grid_map.update()
        print(self.img.shape)



    def clear_map(self):
        self.map = []


    def update(self, show_theoretical_position: bool=False):
        cv2.imshow(self.window_name, self.get_img(show_theoretical_position))
        cv2.waitKey(10)


    def end_sim(self):
        cv2.destroyAllWindows()
    

class OccupancyGridMap:
    def __init__(self, size: set, resolution: float, border: int=3):
        self.resolution = resolution
        self.map = np.full((size[0], size[1]), 0.5, dtype=np.float32)
        self.log_odds = np.log(self.map/(1-self.map))
        self.border = border
        self.p_occ = 0.9
        self.p_free = 1 - self.p_occ
        self.pmi = 0.5  # probability of beeing occupied
    
    def occupancy_grid_mapping(self, lidar_data: np.ndarray, x_pos:float, y_pos:float, angle:float):
        for alpha, distance in lidar_data:
            length_min = distance - self.border
            length_max = distance + self.border
            for x, y in self.bresenhams_stupid_filips_algorithm(x_pos, y_pos, alpha + angle, length_max):
                if np.linalg.norm([x-x_pos, y-y_pos]) > length_min:
                    self.log_odds[x, y] = self.log_odds[x, y] + np.log(self.p_free/self.p_occ) - self.pmi
                else:
                    self.log_odds[x, y] = self.log_odds[x, y] + np.log(self.p_occ/self.p_free) - self.pmi
        
    def bresenhams_stupid_filips_algorithm(self, x_pos:float, y_pos:float, angle:float, length:int):
        for i in range(length.astype(int)):
            yield x_pos + int(np.cos(angle)*i), y_pos + int(np.sin(angle)*i)
    
    def bresenhams_line_algorithm(self, start: np.ndarray, end: np.ndarray):
        pass
    
    def update(self):
        self.map = 1 - 1/(1+np.exp(self.log_odds))
        self.pmi = np.sum(self.map)/(self.map.shape[0]*self.map.shape[1])
    