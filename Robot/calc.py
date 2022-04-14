from math import atan, pi, cos, sin
from Robot import roomX, roomY, cap

def exact_pos(Robot_data, RobotAngle, RobotPos, square):
    pos = []
    for i in range(0, len(Robot_data), 2):
        distance = int(Robot_data[i])+10
        SignalAngle = 90 - int(Robot_data[i+1])
        FullAngle = RobotAngle + SignalAngle
        Fsquare = square
        if FullAngle < 0:
            FullAngle += 90
            if Fsquare == 1:
                Fsquare = 4
            else:
                Fsquare -= 1
        elif FullAngle > 90:
            FullAngle -= 90
            if Fsquare == 4:
                Fsquare = 1
            else:
                Fsquare += 1

        if Fsquare == 2 or Fsquare == 4:
            FullAngle = abs(FullAngle-90)
                
        deltaY = round(sin(FullAngle*pi/180)*distance, 0)
        deltaX = round(cos(FullAngle*pi/180)*distance, 0)
       
        if RobotPos[0]+deltaX < roomX and RobotPos[0]-deltaX > 0 and RobotPos[1]+deltaY < roomY and RobotPos[1]-deltaY > 0:
            if Fsquare == 1:
                pos.append((RobotPos[0]-deltaX, RobotPos[1]-deltaY))
            elif Fsquare == 2:
                pos.append((RobotPos[0]+deltaX, RobotPos[1]-deltaY))
            elif Fsquare == 3:
                pos.append((RobotPos[0]+deltaX, RobotPos[1]+deltaY))
            elif Fsquare == 4:
                pos.append((RobotPos[0]-deltaX, RobotPos[1]+deltaY))
    return pos


def cmPx(avRoomX, avRoomY):
    pixX = cap.get(3)
    pixY = cap.get(4)

    X_cmPx = float(avRoomX/pixX)
    Y_cmPx = float(avRoomY/pixY)
    return X_cmPx, Y_cmPx


def PosAngle(Fcx, Fcy, Bcx, Bcy):
    if Fcy >= Bcy:
        if Fcx >= Bcx:
            square = 3
        else:
            square = 4
    else:
        if Fcx >= Bcx:
            square = 2
        else:
            square = 1


    if Fcx-Bcx == 0:
        angle = 90
    else:
        angle = atan(abs(Fcy-Bcy)/abs(Fcx-Bcx))
        angle = round(angle*180/pi, 0)
        if square == 2 or square == 4:
            angle = abs(angle-90)

    pos = (int((Fcx+Bcx)/2), int((Fcy+Bcy)/2))
    return pos, angle, square