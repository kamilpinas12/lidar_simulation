import numpy as np


class Object():
    def __init__(self, x_pos:float, y_pos:float, move_noise_std:float = 0, rotation_noise_std:float=0, offset:float=0, angle:float=np.pi/2, color1:int=200 , color2:int=50, size:int=10):
        '''
        :param float x_pos: initial x position
        :param float y_pos: inintial y position 
        :param float move_noise_std: standard deviation driving forward 
        :param float rotation_noise_std: standar deviation while turning and going forwad 
        :param float offset: constant noise for rotation and driving straingt
        :param float angle: initial angle 
        :param int color1: upper color of the object range: 1:255
        :param int color2: lower color of the object range: 1:255 
        '''
        if color1 == 0 or color2 == 0:
            raise Exception("color value cannot be 0 ")
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.rotation_noise_std = rotation_noise_std
        self.move_noise_std = move_noise_std
        self.offset = offset

        self.real_x_pos = x_pos
        self.real_y_pos = y_pos
        self.real_angle = angle

        self.x = x_pos
        self.y = y_pos
        self.angle = angle


        '''
        object consists of vector that starts at the center of the object 
        and points at every pixel of the object  
        '''
        self.object_matrix = np.zeros((2, (2*(size+1))**2))
        iter = 0
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                self.object_matrix[:, iter] = np.array([i, j])
                iter += 1



    '''
    function returns position base on input of move function 
    if noise is 0 get_position and get real positon are equal
    '''
    def get_position(self):
        return self.x, self.y, self.angle

    def get_real_position(self):
        return self.real_x_pos, self.real_y_pos, self.real_angle



    def move_raw(self, delta_x: float, delta_y: float, delta_angle:float):
        '''
        move object with by vector [delta_x, delta_y] and rotate by delta_angle
        doesn't include noise !!!
        '''
        self.real_x_pos += delta_x
        self.real_y_pos += delta_y
        self.real_angle += delta_angle


    def rotate(self, angle: float, random_noise: bool=True):
        if self.rotation_noise_std != 0 and random_noise:
            self.real_angle += angle + np.random.randn(1)[0] * self.rotation_noise_std + self.offset
            self.real_y_pos += np.random.rand(1)[0]*self.move_noise_std * 0.01
            self.real_x_pos += np.random.rand(1)[0]*self.move_noise_std * 0.01
        else:
            self.real_angle += angle 
        
        self.angle += angle


    def move(self, y: float, random_noise: bool=True):
        if self.rotation_noise_std != 0 and random_noise:
            noise = self.rotation_noise_std * np.random.randn(1)[0] + self.offset
            self.real_y_pos += np.sin(self.real_angle + noise) * y + np.random.rand(1)[0]*self.move_noise_std
            self.real_x_pos += np.cos(self.real_angle + noise) * y + np.random.rand(1)[0]*self.move_noise_std
            self.x += np.cos(self.real_angle) * y
            self.y += np.sin(self.real_angle) * y
        else:
            dx = np.cos(self.real_angle) * y
            dy = np.sin(self.real_angle) * y
            self.real_y_pos += dy
            self.real_x_pos += dx
            self.x += dx
            self.y += dy


    def rotate_object(self) -> np.ndarray:
        '''
 
        '''
        rotation_matrix = np.array([[np.cos(self.real_angle), -np.sin(self.real_angle)], [np.sin(self.real_angle), np.cos(self.real_angle)]])
        return rotation_matrix.dot(self.object_matrix)
         

    def add_object_to_img(self, img_org: np.ndarray) -> np.ndarray:
        img = img_org.copy()
        rotated_obj = self.rotate_object()
        different_color_counter = self.object_matrix.size//4
        for i in range(self.object_matrix.shape[1]):
            x, y = round(self.real_x_pos+rotated_obj[0, i]), round(self.real_y_pos+rotated_obj[1, i])
            if 0 <= x < img.shape[1] and 0 < y < img.shape[0]:
                if different_color_counter:
                    img[img.shape[0]-y, x] = self.color2 
                    different_color_counter -= 1
                else:
                    img[img.shape[0]-y, x] = self.color1

        return img




