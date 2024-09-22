import pygame as pg

pg.init()
W, H = 480, 640
display = pg.display.set_mode((W, H))

def main():
    while True:
        #1
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        #2
        #3
        display.fill('white')
        pg.display.update()
        pg.time.delay(1000 // 60)

if __name__ == '__main__':
    main()