from ghost import Ghost
from point import Point
from being import Coord
from random import randint
from dataclasses import dataclass
from controller import Controller
import pygame


@dataclass
class Var:
    screen: pygame.display
    width: int
    height: int
    fps: int
    safe_space: int
    num_cols: int
    num_rows: int
    cell_size: int


def are_meet(obj1, obj2):
    return obj1.coord.normal() == obj2.coord.normal()


class InfoDrawer:
    var: Var
    players: list

    def __init__(self, var, players):
        self.var = var
        self.players = players
        self.FONT = pygame.font.Font("Assets/fonts/FuzzyBubbles-Regular.ttf", 20)
        self.LIVE_SIZE = 25
        self.LIVE = pygame.transform.scale(pygame.image.load("Assets/other/heart.png"),
                                           (self.LIVE_SIZE, self.LIVE_SIZE))

    def draw_info(self):
        pygame.draw.rect(self.var.screen, (0, 0, 0),
                         (0, self.var.height - self.var.safe_space, self.var.width, self.var.height))
        for player in self.players:
            score_color = (255, 255, 255)
            if player.how_angry > 0:
                fill_width = self.var.width * player.how_angry // 7500 // len(self.players)
                pygame.draw.rect(self.var.screen, (48, 30, 75),
                                 (self.var.width // 2 * player.index, self.var.height - self.var.safe_space,
                                  fill_width, self.var.height))
                score_color = (239, 64, 115)

            rend_score_pl = self.FONT.render(f"Score: {player.score}", True, score_color)
            rend_lives_pl = self.FONT.render("Lives:", True, score_color)

            score_coord = (self.var.width // 8 + self.var.width // 2 * player.index,
                           self.var.height - self.var.safe_space // 2)
            score_rect_pl = rend_score_pl.get_rect(center=score_coord)

            live_coord = (5 * self.var.width // 16 + self.var.width // 2 * player.index,
                          self.var.height - self.var.safe_space // 2)
            score_lives_pl = rend_lives_pl.get_rect(center=live_coord)

            self.var.screen.blit(rend_score_pl, score_rect_pl)
            self.var.screen.blit(rend_lives_pl, score_lives_pl)

            for i in range(player.lives):
                self.var.screen.blit(self.LIVE, (live_coord[0] + (i + 1) * self.LIVE_SIZE + 10, live_coord[1] - 15))


class Field:
    var: Var
    info_drawer: InfoDrawer
    controller: Controller
    level: dict
    point_map: dict
    ghosts: list
    players: list
    color = (154, 0, 255)
    angry_count: int
    prev_blinky_coord = None

    def __init__(self, screen, width, height, filepath_map, players, fps):
        self.PLAYER_ALLOWED_TYPES = (0, 1, 2, 10, 14, 15)
        self.GHOST_ALLOWED_TYPES = (0, 1, 2, 9, 10, 11, 12, 13, 14, 15)
        self.GHOST_NAMES = ["Blinky", "Clyde", "Inky", "Pinky"]
        num_cols, num_rows = self.init_level(filepath_map)
        safe_space = 50
        cell_size = min((height - safe_space) // num_rows, width // num_cols) // 2 * 2
        self.var = Var(screen, width, height, fps, safe_space, num_cols, num_rows, cell_size)
        self.players = players
        self.info_drawer = InfoDrawer(self.var, self.players)
        for player in players:
            player.set_var(self.var)
        self.controller = Controller()
        self.angry_counter = 0
        self.init_points()
        self.start()

    def init_level(self, filepath_map):
        with open(filepath_map) as file:
            level = eval(file.read())
        num_cols = len(level[0])
        num_rows = len(level)
        self.level = {}
        for i in range(num_cols):
            for j in range(num_rows):
                self.level[i, j] = level[j][i]
        return num_cols, num_rows

    def init_points(self):
        self.point_map = {}
        for i in range(self.var.num_cols):
            for j in range(self.var.num_rows):
                self.point_map[i, j] = []
                if self.level[i, j] in (1, 2):
                    self.point_map[i, j] += [Point(self.var, self.level[i, j], (i, j))]

    def start(self, only=None):
        self.go_to_start(only)
        for player in self.players:
            if only is None or only == player.index:
                player.direction = [0, 0, 0, 0]
                player.new_direction_timeout = 0
        for ghost in self.ghosts:
            ghost.is_eaten = False
            ghost.when_leave = ghost.leave_after_start

    def go_to_start(self, only=None):
        self.ghosts = []
        for i in range(self.var.num_rows):
            for j in range(self.var.num_cols):
                if 14 <= self.level[i, j] <= 15:
                    if only is None or only + 14 == self.level[i, j]:
                        self.players[self.level[i, j] - 14].move_to((i, j))
                if 10 <= self.level[i, j] <= 13:
                    self.ghosts += [Ghost(self.var, (i, j),
                                          self.GHOST_NAMES[self.level[i, j] - 10])]
                    self.ghosts[-1].go_to_start()

    def draw_map(self):
        self.var.screen.fill("black")
        line_width = 2
        for i in range(self.var.num_cols):
            for j in range(self.var.num_rows):
                coord = Coord((i, j), self.var.cell_size, True)
                if self.level[i, j] == 3:
                    pygame.draw.line(self.var.screen, self.color,
                                     coord.px(1, 0), coord.px(1, 2), line_width)
                if self.level[i, j] == 4:
                    pygame.draw.line(self.var.screen, self.color,
                                     coord.px(0, 1), coord.px(2, 1), line_width)
                if self.level[i, j] == 5:
                    pygame.draw.circle(self.var.screen, self.color, coord.px(0, 2),
                                       self.var.cell_size // 2, line_width, draw_top_right=True)
                if self.level[i, j] == 6:
                    pygame.draw.circle(self.var.screen, self.color, coord.px(2, 2),
                                       self.var.cell_size // 2, line_width, draw_top_left=True)
                if self.level[i, j] == 7:
                    pygame.draw.circle(self.var.screen, self.color, coord.px(2, 0),
                                       self.var.cell_size // 2, line_width, draw_bottom_left=True)
                if self.level[i, j] == 8:
                    pygame.draw.circle(self.var.screen, self.color, coord.px(0, 0),
                                       self.var.cell_size // 2, line_width, draw_bottom_right=True)
                if self.level[i, j] == 9:
                    pygame.draw.line(self.var.screen, (0, 255, 205),
                                     coord.px(0, 1), coord.px(2, 1), line_width - 1)
                if 80 <= self.level[i, j] <= 95:
                    current = self.level[i, j] - 80
                    if current % 2:
                        pygame.draw.line(self.var.screen, self.color,
                                         coord.px(0, 1), coord.px(1, 1), line_width)
                    current //= 2
                    if current % 2:
                        pygame.draw.line(self.var.screen, self.color,
                                         coord.px(1, 0), coord.px(1, 1), line_width)
                    current //= 2
                    if current % 2:
                        pygame.draw.line(self.var.screen, self.color,
                                         coord.px(1, 1), coord.px(2, 1), line_width)
                    current //= 2
                    if current % 2:
                        pygame.draw.line(self.var.screen, self.color,
                                         coord.px(1, 1), coord.px(1, 2), line_width)

    def draw_info(self):
        self.info_drawer.draw_info()

    def step(self):
        self.controller.play_music_if_no_sound()
        self.draw_map()
        for player in self.players:
            for i in range(player.speed // self.var.fps):
                col_x, col_y = player.coord.cell()
                player.set_allowed_directions([self.is_allowed(col_x - 1, col_y),
                                               self.is_allowed(col_x, col_y - 1),
                                               self.is_allowed(col_x + 1, col_y),
                                               self.is_allowed(col_x, col_y + 1)])
                if player.move():
                    self.angry_counter -= 1
                    if not self.angry_counter:
                        self.controller.stop_sound("angry")
                if player.coord.in_cell():
                    col_x, col_y = player.coord.cell()
                    for point in self.point_map[col_x, col_y]:
                        point.get_eaten()
                        if point.category == 2:
                            self.controller.set_sound("angry")
                            player.set_angry()
                            self.angry_counter += 1
                        player.score += 1
                    self.point_map[col_x, col_y] = []
                loser = self.check_meet_ghost()
                if loser:
                    return 3 - loser
        for ghost in self.ghosts:
            for i in range(ghost.get_speed() // self.var.fps):
                if ghost.name == Ghost.NAMES[0] and ghost.is_eaten == 0:
                    self.prev_blinky_coord = ghost.coord
                col_x, col_y = ghost.coord.cell()
                ghost.set_allowed_directions([self.is_allowed(col_x - 1, col_y, True),
                                              self.is_allowed(col_x, col_y - 1, True),
                                              self.is_allowed(col_x + 1, col_y, True),
                                              self.is_allowed(col_x, col_y + 1, True)])
                if ghost.when_leave == 0:
                    all_are_angry = True
                    for player in self.players:
                        if player.how_angry == 0:
                            all_are_angry = False
                    if all_are_angry and not ghost.is_eaten:
                        ghost.set_blind()
                        if ghost.direction == [0, 0, 0, 0] or randint(0, 500) == 0:
                            ghost.set_direction(randint(0, 3))
                    else:
                        ghost.set_direction(self.create_path(ghost.coord,
                                                             ghost.get_target(self.prev_blinky_coord,
                                                                              self.players)))
                ghost.move()
                loser = self.check_meet_ghost()
                if loser:
                    return 3 - loser
        is_win = True
        for cell in self.point_map:
            for point in self.point_map[cell]:
                point.draw()
                is_win = False
        for being in self.players + self.ghosts:
            being.draw()
        self.draw_info()
        if is_win:
            self.controller.set_sound("victory", True, True)
            return 3
        return 0

    def is_allowed(self, x, y, ghost_ready=False):
        if ghost_ready:
            return self.level[x % self.var.num_cols, y % self.var.num_rows] in self.GHOST_ALLOWED_TYPES
        return self.level[x % self.var.num_cols, y % self.var.num_rows] in self.PLAYER_ALLOWED_TYPES

    def create_path(self, coord, target):
        if not coord.in_cell():
            return -1
        approached = [[-1] * self.var.num_rows for _ in range(self.var.num_cols)]
        # bfs for finding the shortest path
        # queue using two stacks
        st_in, st_out = [], [(i[0] % self.var.num_cols, i[1] % self.var.num_rows, 0, False) for i in target]
        while st_out != [] or st_in != []:
            if not st_out:
                st_out = st_in[::-1]
                st_in = []
            x, y, direction, allowed_prev = st_out.pop()
            if not self.is_allowed(x, y, True) and allowed_prev or approached[x][y] != -1:
                continue
            if (x, y) == coord.cell():
                return direction
            approached[x][y] = 0
            for cell in [((x + 1) % self.var.num_cols, y, 0), ((x - 1) % self.var.num_cols, y, 2),
                         (x, (y + 1) % self.var.num_rows, 1), (x, (y - 1) % self.var.num_rows, 3)]:
                st_in += [cell + (self.is_allowed(x, y, True),)]
        return -1

    def check_meet_ghost(self):
        for player in self.players:
            for ghost in self.ghosts:
                if are_meet(player, ghost) and not ghost.is_eaten:
                    meet_type = player.meet_ghost(ghost)
                    if meet_type:
                        if meet_type == 1:
                            self.controller.set_sound("restart", True, True)
                        else:
                            self.controller.set_sound("death")
                        self.start(player.index)
                        if player.lives == 0:
                            return player.index + 1
                    else:
                        self.controller.set_sound("eaten")
                        player.score += 30
                        if ghost.name == Ghost.NAMES[0]:
                            self.prev_blinky_coord = None
        return 0
