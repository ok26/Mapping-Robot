from Robot.Orientation import find_markers
from Robot import low_Robot1, high_Robot1, low_Robot2, high_Robot2, room, cap, s
from Robot.Connect import check_kBoardInp
from Robot.calc import exact_pos, cmPx, PosAngle
import matplotlib.pyplot as plt
import cv2
import numpy as np


####################################################################################################
#   Try to fix remove fake dots by removing eferything in distance upuntil distnace point
####################################################################################################

def run():

    while True:
        _, frame = cap.read()
        cv2.imshow('img1',frame)
        if cv2.waitKey(1) & 0xFF == ord('y'): 
            cv2.destroyAllWindows()
            break

    avRoomX = int(input("Camera width cm: "))
    avRoomY = int(input("Camera height cm: "))
    Xcm_pixel, Ycm_pixel = cmPx(avRoomX, avRoomY)
    startX = int(room.shape[1]/2) - int(avRoomX/2)
    startY = int(room.shape[0]/2) - int(avRoomY/2)

    while True:
        Fcx, Fcy = find_markers((low_Robot1, high_Robot1))
        Bcx, Bcy = find_markers((low_Robot2, high_Robot2))

        if len(Fcx) != 1 or len(Fcy) != 1 or len(Bcx) != 1 or len(Bcy) != 1:
            continue

        Fcx, Bcx, Fcy, Bcy = Fcx[0], Bcx[0], Fcy[0], Bcy[0]
        

        RobotPos, RobotAngle, square = PosAngle(Fcx, Fcy, Bcx, Bcy)
        RobotPos = (startX + int(round(RobotPos[0]*Xcm_pixel, 0)), startY + int(round(RobotPos[1]*Ycm_pixel, 0)))

        print(RobotAngle, square, RobotPos)

        room[np.where(room==2)] = 0

        room[RobotPos[1]-3:RobotPos[1]+3,RobotPos[0]-3:RobotPos[0]+3][np.where(room[RobotPos[1]-3:RobotPos[1]+3,RobotPos[0]-3:RobotPos[0]+3] != 1)] = 2
            
        Robot_data = check_kBoardInp()
        if Robot_data == "quit":
            break
        elif Robot_data != []:
            positions = exact_pos(Robot_data, RobotAngle, RobotPos, square)
            for pos in positions:
                room[int(pos[1]),int(pos[0])] = 1
            plt.imshow(np.rot90(room))
            plt.pause(0.1)
        

    s.send(str("quit").encode())
    s.close()
    np.savetxt("Robot/SavedRoom.txt", room)
    plt.imshow(np.rot90(room))
    plt.show()