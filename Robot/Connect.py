import keyboard
from Robot import s

def check_kBoardInp():
    data = []
    if keyboard.is_pressed("space"):                       
        s.send(str("checkSur").encode())
        while True:
            recv_data = s.recv(1024).decode()
            if recv_data[-4:] == "181 ":
                break
            else:
                data += [x for x in recv_data.split(" ")[:-1]]
    elif keyboard.is_pressed("esc"):
        data = "quit"

    return data