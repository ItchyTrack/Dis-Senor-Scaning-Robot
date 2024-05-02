import web
from time import sleep
from robot import Robot

robot = Robot()

web.startWebsite(robot)

while True:
    sleep(0.01)
    robot.update()