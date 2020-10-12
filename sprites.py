import pygame
from pygame.locals import *
from settings import *
vect = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.sprite_idle[0]
        self.rect = self.image.get_rect()
        #self.rect.center = (SIZE[0] / 2, SIZE[1] / 2)
        self.velocity = vect(0, 0)
        self.acceleration = vect(0, 0)
        self.position = vect(self.rect.height, self.rect.width)
        self.walking = False
        self.jumping = False

    def load_images(self):
        path ='img/sprites/'
        self.sprite_idle = (pygame.image.load(path + "idle/adventurer-idle-00.png").convert(), pygame.image.load(path + "idle/adventurer-idle-01.png").convert(), pygame.image.load(path + "idle/adventurer-idle-02.png").convert())
        self.sprite_run_r = (pygame.image.load(path + "run/adventurer-run-00.png").convert(), pygame.image.load(path + "run/adventurer-run-01.png").convert(), pygame.image.load(path + "run/adventurer-run-02.png").convert(),
                    pygame.image.load(path + "run/adventurer-run-03.png").convert(), pygame.image.load(path + "run/adventurer-run-04.png").convert(), pygame.image.load(path + "run/adventurer-run-05.png").convert())
        self.sprite_jump_r = (pygame.image.load(path +"jump/adventurer-jump-00.png").convert(), pygame.image.load(path +"jump/adventurer-jump-01.png").convert(), pygame.image.load(path +"jump/adventurer-jump-02.png").convert(),
                             pygame.image.load(path +"jump/adventurer-jump-03.png").convert(), pygame.image.load(path +"jump/adventurer-jump-04.png").convert())
        self.sprite_run_l = []
        self.sprite_jump_l = []
        for s in self.sprite_run_r:
            self.sprite_run_l.append(pygame.transform.flip(s, True, False))
        for s in self.sprite_jump_r:
            self.sprite_jump_l.append(pygame.transform.flip(s, True, False))

    def jump(self):
        self.velocity.y = -5
        self.jumping = True

    def update(self):
        self.animate()
        self.acceleration = vect(0, GRAV)
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]):
            self.acceleration.x = -PLAYER_ACC
        if (keys[K_RIGHT] or keys[K_d]):
            self.acceleration.x = PLAYER_ACC

        # Movement
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.5:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.center = self.position

        if self.position.x > SIZEUP[0]:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = SIZEUP[0]
        self.rect.midbottom = self.position

    def animate(self):
        now = pygame.time.get_ticks()
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                bottom = self.rect.bottom
                if self.velocity.x > 0 and not self.jumping:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_run_r)
                    self.image = self.sprite_run_r[self.current_frame]
                elif self.velocity.x < 0 and not self.jumping:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_run_l)
                    self.image = self.sprite_run_l[self.current_frame]
                elif self.velocity.x > 0 and self.jumping:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_r)
                    self.image = self.sprite_jump_r[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_l)
                    self.image = self.sprite_jump_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping and not self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                bottom = self.rect.bottom
                self.current_frame = (self.current_frame + 1) % len(self.sprite_idle)
                self.image = self.sprite_idle[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platforms(pygame.sprite.Sprite):
    def __init__(self, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.x = col
        self.y = row
        self.rect.x = col * TILE_SIZE
        self.rect.y = row * TILE_SIZE