import pygame as pg

pg.init()
W, H = 480, 640
display = pg.display.set_mode((W, H))

GRAVITY = 1
JUMP = -30
PLATFORM_WIDTH = 105
MIN_GAP = 90
MAX_GAP = 180

class PLayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_left = pg.image.load('img/doodle_left.png')
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect(center=(W//2, H//2))
        self.speed = 0

    def draw(self):
        if self.rect.y > H:
            # ТУТ ПОТОМ СДЕЛАЕМ ГЕЙМ ОВЕР (но пока респавн для теста)
            self.rect.y = H//2
        else:
            display.blit(self.image, self.rect)

    def update(self):
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


doodle = PLayer()
def main():
    while True:
        #1
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        #2
        doodle.update()
        #3
        display.fill('white')
        doodle.draw()
        pg.display.update()
        pg.time.delay(1000 // 60)

if __name__ == '__main__':
    main()