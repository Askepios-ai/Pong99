import socket
import time
import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        self.players = {}
        self.mouse_pos = (0,0)

    def draw_players(self):
        for player, state in self.players.items():
            self.screen.fill((255,255,255), (state.x, state.y, 10, 40))

    def game_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setblocking(False)
            while True:
                pygame.event.pump()
                self.mouse_pos = pygame.mouse.get_pos()
                message = "{}".format(self.mouse_pos[1])
                s.sendto(message.encode(), ("127.0.0.1",43567))
                try:
                    data = s.recvfrom(1024)
                    parsed_data = str(data)
                except:
                    time.sleep(0.005)
                else:
                    parsed_data = data[0].decode()
                    player_id = ",".join(parsed_data.split(",")[:2])
                    player_pos = parsed_data.split(",")[2:]
                    if player_id not in self.players:
                        self.players[player_id] = Player()
                        print("ADDED NEW PLAYER")
                    self.players[player_id].x = int(player_pos[0])
                    self.players[player_id].y = int(player_pos[1])
                self.screen.fill((0,0,0))
                self.draw_players()
                pygame.display.flip()

if __name__ == "__main__":
    g = Game()
    g.game_loop()
