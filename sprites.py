from settings import *
import pytmx
from exceptions import *


def color_key(sprite):
    for s in sprite:
        s.set_colorkey(BLACK)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.sprite_idle_r[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movement = [0, 0]
        self.momentum = 0
        self.move_r = False
        self.move_l = False
        self.facing_r = True
        self.facing_l = False
        self.jump_time = 0
        self.jumping = False
        self.falling = False
        self.death = 0

    def load_images(self):
        try:
            path = 'assets/img/sprites/'
            self.sprite_idle_r = [pygame.image.load(path + "idle/adventurer-idle-0%s.png" % frame) for frame in range(0, 3)]
            self.sprite_run_r = [pygame.image.load(path + "run/adventurer-run-0%s.png" % frame) for frame in range(0, 6)]
            self.sprite_jump_r = [pygame.image.load(path + "jump/adventurer-jump-0%s.png" % frame) for frame in range(0, 5)]
            self.sprite_idle_l = []
            self.sprite_run_l = []
            self.sprite_jump_l = []
            for s in self.sprite_idle_r:
                self.sprite_idle_l.append(pygame.transform.flip(s, True, False))
            for s in self.sprite_run_r:
                self.sprite_run_l.append(pygame.transform.flip(s, True, False))
            for s in self.sprite_jump_r:
                self.sprite_jump_l.append(pygame.transform.flip(s, True, False))
            color_key(self.sprite_idle_l)
            color_key(self.sprite_idle_r)
            color_key(self.sprite_run_l)
            color_key(self.sprite_run_r)
            color_key(self.sprite_jump_l)
            color_key(self.sprite_jump_r)
        except pygame.error as err:
            pygame_error(err)

        except FileNotFoundError as err:
            filenotfound_error(err)

    def update(self):
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if self.move_l or self.move_r:
            if now - self.last_update > 100:
                self.last_update = now
                if self.move_r and not self.jumping and not self.falling:
                    self.facing_l = False
                    self.facing_r = True
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_run_r)
                    self.image = self.sprite_run_r[self.current_frame]
                elif self.move_l and not self.jumping and not self.falling:
                    self.facing_l = True
                    self.facing_r = False
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_run_l)
                    self.image = self.sprite_run_l[self.current_frame]
                elif self.move_r and self.jumping:
                    self.facing_l = False
                    self.facing_r = True
                    if self.current_frame < 3:
                        self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_r)
                    self.image = self.sprite_jump_r[self.current_frame]
                elif self.move_l and self.jumping:
                    self.facing_l = True
                    self.facing_r = False
                    if self.current_frame < 3:
                        self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_l)
                    self.image = self.sprite_jump_l[self.current_frame]
                elif self.move_r and self.falling:
                    self.facing_l = False
                    self.facing_r = True
                    self.image = self.sprite_jump_r[3]
                elif self.move_l and self.falling:
                    self.facing_l = True
                    self.facing_r = False
                    self.image = self.sprite_jump_l[3]
        if self.jumping and not self.move_r and not self.move_l:
            if now - self.last_update > 100:
                self.last_update = now
                if self.facing_r and not self.facing_l:
                    if self.current_frame < 3:
                        self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_r)
                    self.image = self.sprite_jump_r[self.current_frame]
                else:
                    if self.current_frame < 3:
                        self.current_frame = (self.current_frame + 1) % len(self.sprite_jump_l)
                    self.image = self.sprite_jump_l[self.current_frame]
        if not self.jumping and not self.move_r and not self.move_l:
            if now - self.last_update > 150:
                self.last_update = now
                if self.facing_r and not self.facing_l:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_idle_r)
                    self.image = self.sprite_idle_r[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.sprite_idle_l)
                    self.image = self.sprite_idle_l[self.current_frame]
        if self.falling:
            if now - self.last_update > 100:
                self.last_update = now
                if self.facing_r and not self.facing_l:
                    self.image = self.sprite_jump_r[3]
                else:
                    self.image = self.sprite_jump_l[3]


class Platforms(pygame.sprite.Sprite):
    def __init__(self, group, x, y, w, h):
        self.group = group
        pygame.sprite.Sprite.__init__(self, self.group)
        self.rect = pygame.Rect(x, y, w, h, color=WHITE)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelaphal=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        y = -target.rect.y + SIZEUP[1] / 2
        if target.rect.y >= self.height - 160:
            y = self.camera.y
        x = -target.rect.x + SIZEUP[0] / 2
        if target.rect.x >= self.width - 250:
            x = self.camera.x
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Button:
    def __init__(self, x, y, path_img):
        try:
            self.img_circle = pygame.image.load(path_img)
            self.img_txt = pygame.image.load('assets/img/UI/ui4.png')
            self.circle_rect = self.img_circle.get_rect()
            self.img_circle = pygame.transform.scale(self.img_circle, (int(self.circle_rect.width * 1.5), int(self.circle_rect.height * 1.5)))
            self.circle_rect = self.img_circle.get_rect()
            self.txt_rect = self.img_txt.get_rect()
            self.img_txt = pygame.transform.scale(self.img_txt, (int(self.txt_rect.width * 1.5), int(self.txt_rect.height * 1.5)))
            self.txt_rect = self.img_txt.get_rect()
            self.circle_rect.x = x
            self.circle_rect.y = y
            self.txt_rect.x = self.circle_rect.x + self.circle_rect.width - 1
            self.txt_rect.y = y + 5

        except pygame.error as err:
            pygame_error(err)

        except FileNotFoundError as err:
            filenotfound_error(err)
