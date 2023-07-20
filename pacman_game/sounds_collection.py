import pygame

pygame.mixer.init()
pygame.init()


class SoundsCollection:
    sounds = {
        "angry": pygame.mixer.Sound("Assets/sounds/angry.wav"),
        "death": pygame.mixer.Sound("Assets/sounds/death.wav"),
        "eaten": pygame.mixer.Sound("Assets/sounds/eaten.wav"),
        "restart": pygame.mixer.Sound("Assets/sounds/restart.wav"),
        "victory": pygame.mixer.Sound("Assets/sounds/victory.wav")
    }

    len_sounds = {
        "angry": int(sounds["angry"].get_length()) * 1000,
        "death": int(sounds["death"].get_length()) * 1000 // 10 * 6,
        "eaten": int(sounds["eaten"].get_length()) * 1000,
        "restart": int(sounds["restart"].get_length() + 1) * 1000,
        "victory": int(sounds["death"].get_length()) * 1000 + 1500
    }
