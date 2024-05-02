if __name__ == "__main__":
    import main
    exit()

from copy import copy
import math

class Drive:
    def __init__(self, wheelDiameter, wheelDistance, startPos = None, startRot = None) -> None: #DL, DR
        self.wheelCircumference = wheelDiameter * math.pi
        self.turnCircumference = wheelDistance * math.pi
        if startPos == None:
            startPos = [0, 0]
        self.pos = startPos
        
        if startRot == None:
            startRot = 0
        self.rot = startRot

    def update(self, moves:list[str]):
        moves = copy(moves)
        stepSize = 1.8
        
        wheelRotationAmoutLeft = 0
        wheelRotationAmoutRight = 0
        
        if "f" in moves and "b" in moves:
            moves.remove("f")
            moves.remove("b")

        if "l" in moves and "r" in moves:
            moves.remove("l")
            moves.remove("r")

        if "f" in moves:
            if "l" in moves:
                wheelRotationAmoutLeft = 0
                wheelRotationAmoutRight = stepSize
            elif "r" in moves:
                wheelRotationAmoutLeft = stepSize
                wheelRotationAmoutRight = 0
            else:
                wheelRotationAmoutLeft = stepSize
                wheelRotationAmoutRight = stepSize
        elif "b" in moves:
            if "l" in moves:
                wheelRotationAmoutLeft = -stepSize
                wheelRotationAmoutRight = 0
            elif "r" in moves:
                wheelRotationAmoutLeft = 0
                wheelRotationAmoutRight = -stepSize
            else:
                wheelRotationAmoutLeft = -stepSize
                wheelRotationAmoutRight = -stepSize
        elif "l" in moves:
            wheelRotationAmoutLeft = -stepSize
            wheelRotationAmoutRight = stepSize
        elif "r" in moves:
            wheelRotationAmoutLeft = stepSize
            wheelRotationAmoutRight = -stepSize

        # tell robot to move

        self.simMove(wheelRotationAmoutLeft, wheelRotationAmoutRight)


    def simMove(self, rotL, rotR):
        amountL = rotL/360 * self.wheelCircumference
        amountR = rotR/360 * self.wheelCircumference
        if amountL == 0 and amountR == 0:
            return
        forward = (amountL + amountR) / 2
        rot = ((amountL - amountR) / 2) / self.turnCircumference * 360
        if rot == 0:
            self.pos[0] += math.cos(math.radians(self.rot)) * forward
            self.pos[1] += math.sin(math.radians(self.rot)) * forward
        else:
            self.pos[0] += math.degrees((math.sin(math.radians(self.rot+rot)) - math.sin(math.radians(self.rot)))/rot) * forward
            self.pos[1] += math.degrees((math.cos(math.radians(self.rot)) - math.cos(math.radians(self.rot+rot)))/rot) * forward
        self.rot += rot