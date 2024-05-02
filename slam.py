if __name__ == "__main__":
    import main
    exit()

import numpy as np
import math
from bin import Bin


class SLAM:
    def __init__(self) -> None:
        self.world = Bin(4, -1, 1, "add")

    def rotateAndTransformPoints(points, x, y, r, arrayToAddTo=None):
        if arrayToAddTo == None:
            arrayToAddTo = []
        for point in points:
            arrayToAddTo.append(
                [
                    point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
                    point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y,
                ]
            )
        return arrayToAddTo


    def rotatePoints(points, sinr, cosr, arrayToAddTo=None):
        if arrayToAddTo == None:
            arrayToAddTo = []
        for point in points:
            arrayToAddTo.append([point[0] * cosr + point[1] * -sinr, point[0] * sinr + point[1] * cosr])
        return arrayToAddTo


    def rotateAndTransformPoint(point, x, y, r):
        return [
            point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
            point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y,
        ]


    def doSlam(self, points, notPointsArrays):
        # print("slam")
        # print(points)
        # print(notPointsArrays)
        notPoints = np.ndarray((0, 2))
        for notPointsArray in notPointsArrays:
            notPoints = np.concatenate((notPoints, notPointsArray[0:-1]))

        self.world.binPoints(points, 1)
        self.world.binPoints(notPoints, -1)
