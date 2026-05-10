from pygame import *
from random import randint
import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect  = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 40)

monsters = sprite.Group()

for i in range(5):
    monsters.add(Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5)))

bullets = sprite.Group()


reload = False
reload_tme = 0
bullets_count = 5
reload_text = font1.render('Reloading...', True, (0, 0, 180))



finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if not reload:
                    fire_sound.play()
                    ship.fire()
                    bullets_count -= 1
                    if bullets_count <= 0:
                        reload = True
                        reload_tme = timer.time()
                        

    ship.update()
    monsters.update()

    sprite_coll = sprite.groupcollide(
    monsters, bullets, True, True
    )


    for i in sprite_coll:
        score += 1
        monster = (Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5)))
        monsters.add(monster)


    if score >= 5:
        finish = True
        lose = font1.render('YOU WIN!', True, (180, 0, 0))
        window.blit(lose, (200, 200))

    if lost >= 3 or sprite.spritecollide(ship, monsters, False):
        finish = True
        lose = font1.render('YOU LOSE', True, (180, 0, 0))
        window.blit(lose, (200, 200))

    if not finish:
        window.blit(background, (0, 0))
        monsters.draw(window)
        bullets.draw(window)
        if reload:
            if timer.time() - reload_tme >= 3:
                reload = False
                bullets_count = 5
            else:
                window.blit(reload_text, (300, 10))
            

        ship.reset()
       
        text = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 50))
        bullets.update()
        
        
    display.update()
    time.delay(60)
