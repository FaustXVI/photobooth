import pygame
import time


class Screen:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        screen_info = pygame.display.Info()
        screen_dimensions = (screen_info.current_w, screen_info.current_h)
        self.screen = pygame.display.set_mode(screen_dimensions, pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size()).convert()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def update_display(self, message: str, background_color: str = "black", size: int = 800, duration = 1):
        self.background.fill(pygame.Color(background_color))
        font = pygame.font.Font(None, size)
        text = font.render(message, 1, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().centery
        self.background.blit(text, textpos)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        time.sleep(duration)

    def show_image(self, image_path):
        self.screen.fill(pygame.Color("white"))
        img = pygame.image.load(image_path)
        img = img.convert()
        (screen_width, screen_height) = self.screen.get_size()
        x = (screen_width / 2) - (img.get_width() / 2)
        y = (screen_height / 2) - (img.get_height() / 2)
        self.screen.blit(img, (x, y))
        pygame.display.flip()

    def show_picture(self, file, duration = 3):
        self.background.fill((0, 0, 0))
        img = pygame.image.load(file)
        img = pygame.transform.scale(img, self.screen.get_size())
        self.background.blit(img, (0, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        time.sleep(duration)
