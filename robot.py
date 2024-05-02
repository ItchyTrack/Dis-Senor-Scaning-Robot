if __name__ == "__main__":
    import main

    exit()

import math
import numpy as np
import cv2
from fakeCar import robotSensor
from drive import Drive
from slam import SLAM

border = 0

class Robot:
    def __init__(self) -> None:
        self.slam = SLAM()
        self.world = self.slam.world
        self.drive = Drive(40, 20)
        self.moves = []  # "f", "b", "l", "r"

    def update(self):
        self.drive.update(self.moves)
        points, notPoints = robotSensor.update(self)
        self.slam.doSlam(points, notPoints)
        # print(self.drive.pos, self.drive.rot)

    def getImage(self):
        scaleAmout = 2#self.world.binSize
        map = cv2.resize(
            cv2.cvtColor(
                ((self.world.array - self.world.minVal) / (self.world.maxVal - self.world.minVal) * 255).astype(np.uint8),
                cv2.COLOR_GRAY2RGB,
            ),
            (0, 0),
            fx=scaleAmout,
            fy=scaleAmout,
            interpolation=cv2.INTER_NEAREST,
        )
        
        x = int((self.drive.pos[0]/self.world.binSize + self.world.xShift) * scaleAmout)
        y = int((self.drive.pos[1]/self.world.binSize + self.world.yShift) * scaleAmout)
        min_x = min(x, -border)
        min_y = min(y, -border)
        max_x = max(x, map.shape[1] + border)
        max_y = max(y, map.shape[0] + border)
        if min_x < 0:
            x -= min_x
            x -= min_x
        if min_y < 0:
            y -= min_y
            y -= min_y

        img = None
        if min_x < 0 or min_y < 0 or max_x >= map.shape[1] or max_y >= map.shape[0]:
            img = np.zeros((max_y - min_y + 2, max_x - min_x + 2, map.shape[2]))
            img[-min_y : map.shape[0] - min_y, -min_x : map.shape[1] - min_x, 0:map.shape[2]] = map

        

        cv2.circle(img, (int(x), int(y)), 2*scaleAmout, (0, 0, 255), -1)
        cv2.circle(img, (int(x + math.cos(math.radians(self.drive.rot))*scaleAmout), int(y + math.sin(math.radians(self.drive.rot))*scaleAmout)), 1*scaleAmout, (0, 255, 0), -1)
        
        # img = cv2.resize((np.arange(0, 100)*2.55).reshape((10, 10)).astype(np.int8), (0,0), fx=10, fy=10, interpolation = cv2.INTER_NEAREST)
        return img  # np.dstack(cv2Image)
