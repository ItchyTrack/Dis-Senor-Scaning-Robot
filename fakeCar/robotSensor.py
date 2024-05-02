from dda import dda
from fakeCar import raycaster

rot = 0
dir = 1
rotSensorAngle = 90

def update(robot):
    global rot, dir, rotSensorAngle
    points = []
    notPointsArrays = []
    for i in range(1):
        rot += dir * 1.8
        hit, pos = raycaster.raycast(robot.drive.pos[0], robot.drive.pos[1], rot + robot.drive.rot, 200, 0)
        notPoints = dda(robot.drive.pos[0]/robot.world.binSize, robot.drive.pos[1]/robot.world.binSize, pos[0]/robot.world.binSize, pos[1]/robot.world.binSize)
        if len(notPoints) != 1:
            for point in notPoints:
                point[0] = point[0] * robot.world.binSize
                point[1] = point[1] * robot.world.binSize
            notPointsArrays.append(notPoints)
        if hit:
            points.append(pos)
        if rot >= rotSensorAngle:
            dir *= -1
        elif rot <= -rotSensorAngle:
            dir *= -1
    return points, notPointsArrays
        