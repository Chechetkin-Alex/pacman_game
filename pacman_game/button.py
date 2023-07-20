import pygame


class Button:
    text_inside = ""
    font = ""
    color = ""
    size = (0, 0)
    rendered_text = object()
    img = object()
    screen = object()

    def __init__(self, screen, coord, text_inside, font, color):
        self.screen = screen
        self.coord = coord
        self.text_inside = text_inside
        self.font = font
        self.color = color
        self.rendered_text = self.font.render(self.text_inside, True, "White")
        self.text_rect = self.rendered_text.get_rect(center=self.coord)
        self.size = (self.rendered_text.get_size()[0] * 1.3, self.rendered_text.get_size()[1] * 1.1)
        self.img = pygame.Surface(self.size, pygame.SRCALPHA)
        self.background = self.img.get_rect(center=(self.coord[0], self.coord[1]))

    def draw(self):
        pygame.draw.rect(self.img, self.color, self.img.get_rect(), 1)
        self.screen.blit(self.img, self.background)
        self.screen.blit(self.rendered_text, self.text_rect)

    def is_pressed(self, coord):
        x_hit = self.background.left <= coord[0] <= self.background.right
        y_hit = self.background.top <= coord[1] <= self.background.bottom
        return x_hit and y_hit
