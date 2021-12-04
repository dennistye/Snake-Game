# Dennis Tye
# CPSC 386-01
# 11/26/2021
# dennis.tye@csu.fullerton.edu
#
# Snake Game
#
# This my Scene File

import math
import pygame

from player import Player, Food
from scores import Scores
class Scene:
    def __init__(self):
        self.next = self
    def change_scene(self, next_scene):
        self.next = next_scene
    def end_scene(self):
        self.change_scene(None)

class TitleScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.title = 'Snake Game'
        self._title_size = 72
        self._d_x = 0.12
        self._d_r = 0.01
        self._d_g = 0.02
        self._d_b = 0.03
        self._x = 0
        self._r = 0
        self._g = 0
        self._b = 0
        self._title_color = (0, 0, 0)
        self.title_font = pygame.font.SysFont(None, self._title_size)
        self.title_img = self.title_font.render('TitleScene', True, (self._r, self._g, self._b))
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.change_scene(RulesScene())
    def update(self):
        self._x += self._d_x % (2 * math.pi)
        self._title_size = 72 + int(4*math.cos(self._x))
        self._r += self._d_r % (255)
        self._g += self._d_g % (255)
        self._b += self._d_b % (255)

        title_r = int(255/2*(math.cos(self._r) + 1))
        title_g = int(255/2*(math.cos(self._g) + 1))
        title_b = int(255/2*(math.cos(self._b) + 1))
        self._title_color = (title_r, title_g, title_b)

        self.title_font = pygame.font.SysFont(None, self._title_size)
        self.title_img = self.title_font.render(self.title, True, self._title_color)
    def draw(self, screen):
        screen.fill((0, 0, 225))

        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, screen_h/2)))

        text_font = pygame.font.SysFont(None, 24)
        text_img = text_font.render('Press Enter To Continue...', True, (0, 0, 0))
        screen.blit(text_img, text_img.get_rect(center=(screen_w/2, screen_h-50)))

class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._player = Player()
        self._food = Food()
        self._game_time = pygame.time.get_ticks()
    def handle_input(self, events):
        for event in events:
            self._player.handle_input(event)
    def update(self):
        self._player.update()
        if self._player.collides(self._food):
            self._player.increment_score()
            self._food.update()
        if not self._player.alive():
            self.change_scene(GameOverScene(self._player.get_score()))

    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((0, 0, 225))
        font = pygame.font.SysFont(None, 24)
        time_elapsed = (pygame.time.get_ticks() - self._game_time) / 1000

        self._player.draw(screen)
        self._food.draw(screen)
        img_str = 'Score:  {}    Time:  {}'.format(self._player.get_score(), int(time_elapsed))
        img = font.render(img_str, True, (0, 0, 0))
        screen.blit(img, (325, 50))

class GameOverScene(Scene):
    def __init__(self, ending_score=0):
        Scene.__init__(self)
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_img = self.title_font.render('GAME OVER', True, (0, 0, 0))

        self.text_font = pygame.font.SysFont(None, 24)
        self.text_img = self.text_font.render('Press Enter to Try Again...', True, (0, 0, 0))

        self._scores = Scores(ending_score)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._scores.save_scores()
                self.change_scene(GameScene())
    def update(self):
        pass
    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((0, 0, 225))
        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.text_img, self.text_img.get_rect(center=(screen_w/2, screen_h-50)))
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, 50)))
        self._scores.draw(screen)
    def end_scene(self):
        self._scores.save_scores()
        self.change_scene(None)

class RulesScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_img = self.title_font.render('Game Rules', True, (0, 0, 0))

        self._rules = ''
        self.rules_font = pygame.font.SysFont(None, 24)
        self.rules_img = self.rules_font.render('Press Enter to\n Try Again...', True, (0, 0, 0))

        self._image = pygame.image.load('Game_rules.png')
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.change_scene(GameScene())
    def update(self):
        pass
    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((0, 0, 225))
        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, 50)))
        screen.blit(self.rules_img, self.rules_img.get_rect(center=(screen_w/2, screen_h-50)))
        screen.blit(self._image, (0, 0))