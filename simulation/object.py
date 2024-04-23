import numpy as np


class Object():
    def __init__(self, x_pos:float, y_pos:float, angle:float=np.pi/2, color1:int=200 , color2:int=50, size:int=10):
        if color1 == 0 or color2 == 0:
            raise Exception("color value cannot be 0 ")
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle = angle         

        self.object_matrix = np.zeros((2, (2*(size+1))**2))
        iter = 0
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                self.object_matrix[:, iter] = np.array([i, j])
                iter += 1


    def rotate_object(self) -> np.ndarray:
        rotation_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)], [np.sin(self.angle), np.cos(self.angle)]])
        return rotation_matrix.dot(self.object_matrix)
         

    def add_object_to_img(self, img_org: np.ndarray) -> np.ndarray:
        img = img_org.copy()
        rotated_obj = self.rotate_object()
        different_color_counter = self.object_matrix.size//4
        for i in range(self.object_matrix.shape[1]):
            x, y = round(self.x_pos+rotated_obj[0, i]), round(self.y_pos+rotated_obj[1, i])
            if 0 <= x < img.shape[1] and 0 < y < img.shape[0]:
                if different_color_counter:
                    img[img.shape[0]-y, x] = self.color2 
                    different_color_counter -= 1
                else:
                    img[img.shape[0]-y, x] = self.color1

        return img




