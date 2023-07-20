from field import Field
from player import Player
from button import Button
from random import choice
import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH = 600
HEIGHT = 650
fps = 60

screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_surface = pygame.Surface((WIDTH, HEIGHT))
bg_surface.set_alpha(128)
pygame.display.set_caption("Pacman")
timer = pygame.time.Clock()

player_normal = [f"Assets/players/pl1.png", f"Assets/players/pl2.png",
                 f"Assets/players/pl3.png", f"Assets/players/pl4.png"]
player_angry = [f"Assets/players/pl_angry.png"] * 4
players = []
field: pygame.display
current_maze = None

pygame.mixer.music.load("Assets/music/background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.55)

last_music_pos = last_sound_pos = 0
sound_volume = 0.55

single_player_mazes = [0, 1]
multiplayer_mazes = [2]

font_size = 60
start_width = WIDTH // 2
start_height = int(HEIGHT * 0.2)


def update_players(num_players):
    global players

    players = [Player(0, player_normal, player_angry), Player(1, player_normal, player_angry)][:num_players]


def new_game(mazes=None):
    global field, sound_volume, current_maze

    if mazes is None:
        mazes = [current_maze]
    if len(mazes) == 1:
        current_maze = mazes[0]
    else:
        current_maze = choice([i for i in mazes if i != current_maze])
    field = Field(screen, WIDTH, HEIGHT, f"Assets/mazes/maze{current_maze}.txt", players, fps)
    field.controller.set_sound_volumes(sound_volume)


def font(size):
    return pygame.font.Font("Assets/fonts/FuzzyBubbles-Regular.ttf", size)


def menu():
    while True:
        screen.fill("black")

        text = font(font_size).render("MENU", True, (255, 255, 255))
        text_pos = text.get_rect(center=(start_width, start_height))

        start_button = Button(screen, (start_width, start_height * 2), "PLAY", font(font_size - 10), "White")
        story_button = Button(screen, (start_width, start_height * 2.7), "PREQUEL", font(font_size - 10), "White")
        options_button = Button(screen, (start_width, start_height * 3.4), "OPTIONS", font(font_size - 10), "White")
        exit_button = Button(screen, (start_width, start_height * 4.1), "EXIT", font(font_size - 10), "White")

        screen.blit(text, text_pos)

        buttons = [start_button, story_button, options_button, exit_button]

        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_pressed(mouse_pos):
                    mode = set_mode()
                    if not mode:
                        break
                    prerender(mode)
                    play()
                if story_button.is_pressed(mouse_pos):
                    story()
                if options_button.is_pressed(mouse_pos):
                    options()
                if exit_button.is_pressed(mouse_pos):
                    pygame.quit()
                    quit()
        pygame.display.update()


def play():
    field.step()
    pygame.display.flip()
    timer.tick(2)

    while True:
        timer.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause() == -1:
                        return
                if event.key == pygame.K_a:
                    players[0].set_direction_with_timeout(0)
                if event.key == pygame.K_w:
                    players[0].set_direction_with_timeout(1)
                if event.key == pygame.K_d:
                    players[0].set_direction_with_timeout(2)
                if event.key == pygame.K_s:
                    players[0].set_direction_with_timeout(3)
                if event.key == pygame.K_LEFT:
                    players[-1].set_direction_with_timeout(0)
                if event.key == pygame.K_UP:
                    players[-1].set_direction_with_timeout(1)
                if event.key == pygame.K_RIGHT:
                    players[-1].set_direction_with_timeout(2)
                if event.key == pygame.K_DOWN:
                    players[-1].set_direction_with_timeout(3)
        result = field.step()
        if result:
            # win or lose
            for player in players:
                player.lives = 3
                player.how_angry = 0
            if result == 3:
                if len(players) == 1:
                    new_game(single_player_mazes)
                else:
                    new_game(multiplayer_mazes)
            else:
                players[2 - result] = Player(2 - result, player_normal, player_angry)
                new_game()
            pygame.time.wait(1500)
            pygame.mixer.music.play(-1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        pygame.display.flip()


def story():
    with open('Assets/story/story.txt', 'r') as f:
        contents = f.read()
    story_size = 20
    start_y_pos = y_pos = 20
    stop_line = start_height * 0.3
    text_height = blit_text_height(contents, font(story_size))

    while True:
        screen.fill("black")

        mouse_pos = pygame.mouse.get_pos()

        rend_text_height, count_of_paragraphs = blit_text(screen, contents, (20, y_pos), font(story_size))

        story_text = font(font_size).render("STORY", True, (154, 0, 255))
        story_text_pos = story_text.get_rect(center=(start_width * 0.6, stop_line))
        screen.blit(story_text, story_text_pos)

        back_button = Button(screen, (start_width * 1.8, stop_line), "back", font(story_size + 10), "White")
        back_button.draw()

        pygame.draw.line(screen, "white", (0, 1.7 * stop_line), (start_width * 1.5, 1.7 * stop_line))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_pressed(mouse_pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_pos < start_y_pos:
                    y_pos += font(story_size).get_linesize()
                elif event.key == pygame.K_DOWN and abs(y_pos) < rend_text_height * (count_of_paragraphs - 2):
                    y_pos -= font(story_size).get_linesize()

        y_pos = min(y_pos, HEIGHT * 0.95 - text_height)

        pygame.display.update()


def blit_text_height(text, this_font):
    collection = [word.split() for word in text.splitlines()]
    line_height = this_font.get_linesize()
    return len(collection) * line_height


def blit_text(surface, text, pos, this_font):
    collection = [words.split(" ") for words in text.splitlines()]
    space = this_font.size(" ")[0]
    safe_space = 50
    x, y = pos[0], pos[1] + 30
    word_height = 0
    color = (230, 0, 0)
    for lines in collection:
        for word in lines:
            word_surface = this_font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= WIDTH * 0.95:
                x = pos[0]
                y += word_height
            if y + word_height <= safe_space:
                break
            surface.blit(word_surface, (x, y + word_height))
            x += word_width + space
        color = (255, 255, 255)
        x = pos[0]
        y += word_height
    return word_height, len(collection)


def options():
    global last_music_pos, last_sound_pos, sound_volume

    volume_height = frame_height = start_height - 50
    sound_height = volume_height * 3
    music_pos = sound_pos = start_width
    music_min = sound_min = int(start_width * 0.3)
    music_max = sound_max = int(start_width * 1.7)
    music_delta = music_max - music_min
    sound_delta = sound_max - sound_min
    is_playing = True

    while True:
        screen.fill("black")

        mouse_pos = pygame.mouse.get_pos()

        music_text = font(font_size - 10).render("MUSIC", True, (255, 255, 255))
        music_text_pos = music_text.get_rect(center=(start_width, volume_height))
        screen.blit(music_text, music_text_pos)

        sound_text = font(font_size - 10).render("SOUND", True, (255, 255, 255))
        sound_text_pos = sound_text.get_rect(center=(start_width, sound_height))
        screen.blit(sound_text, sound_text_pos)

        if pygame.mouse.get_pressed(3)[0] != 0:
            if music_min <= mouse_pos[0] <= music_max and \
                    volume_height <= mouse_pos[1] <= volume_height * 2.5:
                if not is_playing:
                    pygame.mixer.music.unpause()
                    is_playing = True
                music_pos = int(mouse_pos[0])

                music_volume = round((music_pos - music_min) / music_delta * 0.9 + 0.1, 3)
                pygame.mixer.music.set_volume(music_volume)

            elif sound_min <= mouse_pos[0] <= sound_max and \
                    sound_height * 1.1 <= mouse_pos[1] <= sound_height * 1.4:
                if is_playing:
                    pygame.mixer.music.pause()
                    is_playing = False

                sound_pos = int(mouse_pos[0])

                sound_volume = round((sound_pos - sound_min) / sound_delta * 0.9 + 0.1, 3)
                test_sound = pygame.mixer.Sound("Assets/sounds/eaten.wav")
                pygame.mixer.Sound.set_volume(test_sound, sound_volume)
                pygame.mixer.Sound.play(test_sound)

        if last_music_pos and music_pos == start_width:
            music_pos = last_music_pos
        pygame.draw.rect(screen, (154, 0, 255), (music_pos, volume_height + 40, 10, 50))
        pygame.draw.rect(screen, "white",
                         (music_min - 20, volume_height + 25, int(start_width * 1.5) + 20, frame_height), 1)

        if last_sound_pos and sound_pos == start_width:
            sound_pos = last_sound_pos
        pygame.draw.rect(screen, (154, 0, 255), (sound_pos, sound_height + 40, 10, 50))
        pygame.draw.rect(screen, "white",
                         (sound_min - 20, sound_height + 25, int(start_width * 1.5) + 20, frame_height), 1)

        back_button = Button(screen, (start_width, HEIGHT * 0.9), "back", font(font_size - 10), "White")
        back_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_pressed(mouse_pos):
                    if not is_playing:
                        pygame.mixer.music.unpause()
                    last_music_pos = music_pos
                    last_sound_pos = sound_pos
                    return

        pygame.display.update()


def prerender(mode):
    countdown = ["go!", 1, 2, 3]
    countdown_color = (255, 0, 0)
    booster = False
    timer.tick(1)
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                booster = True

        if not booster:
            screen.fill((0, 0, 0))
            countdown_text = font(50).render(str(countdown[-1]), True, countdown_color)
            countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)

            text = font(30).render("click to skip", True, (255, 255, 255))
            text_pos = text.get_rect(center=(start_width, HEIGHT * 0.9))
            screen.blit(text, text_pos)

            text_for_pl1 = font(30).render("Use WASD to control ", True, (255, 255, 255))
            text_pl1 = font(30).render("player1", True, (51, 153, 255))
            text_pos_for_pl1 = text_for_pl1.get_rect(center=(WIDTH // 2 - text_pl1.get_width() // 2, HEIGHT * 0.73))
            text_pos_pl1 = text_pl1.get_rect(
                center=(text_pos_for_pl1.right + text_pl1.get_width() // 2, HEIGHT * 0.73))
            screen.blit(text_for_pl1, text_pos_for_pl1)
            screen.blit(text_pl1, text_pos_pl1)

            if mode == 2:
                text_for_pl2 = font(30).render("Use arrows to control ", True, (255, 255, 255))
                text_pl2 = font(30).render("player2", True, (255, 133, 51))
                text_pos_for_pl2 = text_for_pl2.get_rect(center=(WIDTH // 2 - text_pl2.get_width() // 2, HEIGHT * 0.8))
                text_pos_pl2 = text_pl2.get_rect(
                    center=(text_pos_for_pl2.right + text_pl2.get_width() // 2, HEIGHT * 0.8))
                screen.blit(text_for_pl2, text_pos_for_pl2)
                screen.blit(text_pl2, text_pos_pl2)

            pygame.display.update()
            timer.tick(1)
            countdown_color = (255, 255 // (len(countdown) + 1), 0)

        countdown.pop()


def pause():
    bg_surface.fill("black")
    screen.blit(bg_surface, (0, 0))
    text_height = start_height // 2

    while True:
        mouse_pos = pygame.mouse.get_pos()

        text = font(font_size).render("PAUSED", True, "white")
        text_pos = text.get_rect(center=(start_width, text_height))
        screen.blit(text, text_pos)

        continue_button = Button(screen, (start_width, text_height * 4.5), "CONTINUE", font(font_size - 10), "White")
        options_button = Button(screen, (start_width, text_height * 6), "OPTIONS", font(font_size - 10), "White")
        back_to_menu_button = Button(screen, (start_width, text_height * 7.5), "BACK TO MENU",
                                     font(font_size - 10), "White")
        for button in [continue_button, options_button, back_to_menu_button]:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu_button.is_pressed(mouse_pos):
                    return -1
                if options_button.is_pressed(mouse_pos):
                    options()
                    field.controller.set_sound_volumes(sound_volume)
                    field.step()
                    screen.blit(bg_surface, (0, 0))
                if continue_button.is_pressed(mouse_pos):
                    return
        pygame.display.flip()


def set_mode():
    mode_height = start_height * 2

    while True:
        screen.fill("black")

        mouse_pos = pygame.mouse.get_pos()

        text = font(font_size).render("Choose your mode", True, (154, 0, 255))
        text_pos = text.get_rect(center=(start_width, start_height))
        screen.blit(text, text_pos)

        single_player_button = Button(screen, (start_width * 0.5, mode_height),
                                      "single", font(font_size), (51, 153, 255))
        multiplayer_button = Button(screen, (start_width * 1.5, mode_height),
                                    "multi", font(font_size), (255, 133, 51))
        back_button = Button(screen, (start_width, HEIGHT * 0.9), "back", font(font_size - 10), "White")

        for button in single_player_button, multiplayer_button, back_button:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_pressed(mouse_pos):
                    return 0
                if single_player_button.is_pressed(mouse_pos):
                    update_players(1)
                    new_game([choice(single_player_mazes)])
                    return 1
                if multiplayer_button.is_pressed(mouse_pos):
                    update_players(2)
                    new_game([choice(multiplayer_mazes)])
                    return 2

        pygame.display.update()


menu()
