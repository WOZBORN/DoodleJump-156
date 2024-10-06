import random

import pygame as pg

pg.init()
W, H = 480, 640
display = pg.display.set_mode((W, H))

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180

score = 0

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    display.blit(img, (x, y))

class Sprite(pg.sprite.Sprite):
    def __init__(self, x ,y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.dead = False

    def update(self):
        super().update()

    def draw(self):
        display.blit(self.image, self.rect)

    def kill(self):
        self.dead = True
        super().kill()


class PLayer(Sprite):
    def __init__(self):
        super().__init__(W//2, H//2, 'img/doodle_left.png')
        self.image_left = self.image
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.speed = 0

    def draw(self):
        if self.dead:
            draw_text("GAME OVER", pg.font.Font(None, 50), 'red', W//2, H//2)
        else:
            display.blit(self.image, self.rect)

    def update(self):
        if self.dead:
            return

        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_left
        if key[pg.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_right

        if self.rect.right < 0:
            self.rect.left = W
        if self.rect.left > W:
            self.rect.right = 0

        self.speed += GRAVITY
        self.rect.y += self.speed

        if self.rect.y > H:
            self.kill()

class BaseBonus(Sprite):
    def __init__(self, image_path: str, plat: 'BasePlatform'):
        img = pg.image.load(image_path)
        w = img.get_width()
        h = img.get_height()
        rect = plat.rect
        x = random.randint(rect.left + w//2, rect.right - w//2)
        y = rect.top - h//2
        super().__init__(x, y, image_path)
        self.platform = plat
        self.dx = self.rect.x - self.platform.rect.x

    def on_collision(self, player):
        global score
        score += 1000
        self.kill()

    def update(self):
        self.rect.x = self.platform.rect.x + self.dx
        if self.platform.dead:
            self.kill()

class Spring(BaseBonus):
    def __init__(self, plat):
        super().__init__('img/spring.png', plat)

    def on_collision(self, player):
        player.speed = -50
        self.image = pg.image.load('img/spring_1.png')


class BasePlatform(Sprite):
    def on_collision(self, player):
        player.speed = JUMP

    def update(self):
        if self.rect.top > H:
            self.kill()

    def attach_bonus(self):
        if random.randint(0, 100) > 90:
            Bonus = random.choice([Spring])
            obj = Bonus(self)
            platforms.add(obj)

class NormalPlatform(BasePlatform):
    def __init__(self, x, y):
        super().__init__(x, y, "img/green.png")

platforms = pg.sprite.Group()

def spawn_platform():
    platform = platforms.sprites()[-1]
    y = platform.rect.y - random.randint(MIN_GAP, MAX_GAP)
    x = random.randint(0, W - PLATFORM_WIDTH)
    types = [NormalPlatform]
    Plat = random.choice(types)
    platform = Plat(x, y)
    platform.attach_bonus()
    platforms.add(platform)

class BaseEnemy(Sprite):
    def update(self):
        if self.rect.top > H:
            self.kill()

    def on_collision(self, player):
        player.kill()

class Hole(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "img/enemy_hole.png")

class LeftRightEnemy(BaseEnemy):
    pass

class UpDownEnemy(BaseEnemy):
    pass

enemies = pg.sprite.Group()

def spawn_enemy(delay):
    if delay > 5000:
        delay = 0
        Enemy = random.choice([Hole])
        x = random.randint(0 , W - 80)
        e = Enemy(x, -H)
        enemies.add(e)
    return delay

doodle = PLayer()

platform = NormalPlatform(W//2 - PLATFORM_WIDTH//2, H - 50)
platforms.add(platform)

def is_top_collision(player: PLayer, platform: BasePlatform):
    if player.rect.colliderect(platform.rect):
        if player.speed > 0:
            if player.rect.bottom < platform.rect.bottom:
                platform.on_collision(player)


def main():
    global score
    passed_time = 0
    while True:
        #1
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        #2
        doodle.update()
        platforms.update()
        enemies.update()
        pg.sprite.spritecollide(doodle, platforms, False, collided=is_top_collision)
        hit_enemy = pg.sprite.spritecollide(doodle, enemies, False)
        if hit_enemy:
            doodle.kill()
        if len(platforms) < 25:
            spawn_platform()
        if doodle.speed < 0 and doodle.rect.bottom < H / 2:
            doodle.rect.y -= doodle.speed
            global score
            score += 1
            for platform in platforms:
                platform.rect.y -= doodle.speed
            for enemy in enemies:
                enemy.rect.y -= doodle.speed
        passed_time = spawn_enemy(passed_time)
        #3
        display.fill('white')
        platforms.draw(display)
        enemies.draw(display)
        doodle.draw()
        if doodle.dead:
            draw_text("GAME OVER", pg.font.Font(None, 50), 'red', W//2, H//2)
            draw_text("Score: " + str(score), pg.font.Font(None, 50), 'red', W//2, H//2 + 50)
            pg.display.update()
            pg.time.delay(2000)
            return
        else:
            draw_text(str(score), pg.font.Font(None, 50), 'black', 10, 10)
        pg.display.update()
        passed_time += pg.time.delay(1000 // 60)

if __name__ == '__main__':
    main()