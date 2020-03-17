import socket
import time

class Player:
    def __init__(self):
        self.left = True
        self.y_pos = 0

    def update(self, data):
        self.y_pos = int(data)

    def get_data(self):
        x = 100
        if not self.left:
            x = 700
        return "{},{}".format(x, self.y_pos)

class Server:
    def __init__(self):
        self.connected = {}

    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("", 43567))
            s.setblocking(False)
            while True:
                self.communication_loop(s)

    def communication_loop(self, s):
        data_waiting = True
        while data_waiting:
            try:
                data = s.recvfrom(1024)
                if data[1] not in self.connected:
                    self.connected[data[1]] = Player()
                    if len(self.connected) > 1:
                        self.connected[data[1]].left = False
                self.connected[data[1]].update(data[0])
            except:
                data_waiting = False
            else:
                self.update_state(data)
        self.send_updates(s)
        time.sleep(0.01)

    def update_state(self, data):
        #print(data)
        pass

    def send_updates(self, socket):
        for address, player in self.connected.items():
            message = "{},{}".format(address, player.get_data())
            for target in self.connected.keys():
                socket.sendto(message.encode(), target)

if __name__ == "__main__":
    s = Server()
    s.serve()
