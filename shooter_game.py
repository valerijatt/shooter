from pygame import *
from random import randint

window = display.set_mode((700,500))
display.set_caption('Шутер')
backround = transform.scale(image.load("christmas.jpg"),( 700,500))
clock = time.Clock()
FPS = 60
mixer.init()
font.init()
sound = mixer.Sound("fire.ogg")
#mixer.music.load("space.ogg")
sound.set_volume(0.01)
#mixer.music.set_volume(0.02)
#mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,player_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), player_size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bulet("ball.png",self.rect.centerx - 7 , self.rect.top, 15, (15,20))
        bulets.add(bullet)
        

        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = randint(-150,-60)
            self.rect.x = randint(50,550)
            global lost
            lost = lost + 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = randint(-150, -60)
            self.rect.x = randint(50, 500)



class Bulet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
                
        
lost = 0
win = 0    
font1 = font.Font(None, 36)
text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
text_win = font1.render("Сбито:" + str(win), 1, (255,255,255))

player = Player("tree.png",315,350,5,(120,150))
enemys = sprite.Group()
for i in range(5):
    enemy = Enemy("grinch.png",randint(50,550),randint(-150,-60),1,(120,150))
    enemys.add(enemy)

bulets = sprite.Group()
finish = False

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("dog.png",randint(50, 550), randint(-150, -60),1,(100,120))
    asteroids.add(asteroid)


game = True
while game:
    clock.tick(FPS)
    display.update()
    window.blit(backround,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish == False:
                sound.play()
                player.fire()
            if e.key == K_SPACE and finish == True:
                finish = False
                enemys = sprite.Group()
                for i in range(5):
                     enemy = Enemy("grinch.png",randint(50,550),randint(-150,-60),1,(120,150))
                     enemys.add(enemy)
                asteroids = sprite.Group()
                for i in range(3):
                    asteroid = Asteroid("dog.png",randint(50, 550), randint(-150, -60),1,(100,120))
                    asteroids.add(asteroid)
                player.rect.x = 315
                win = 0
                lost = 0
                text_win = font1.render("Сбито:" + str(win), 1, (255,255,255))
                bulets = sprite.Group()

    if finish == True:
        window.blit(won, (240,250))
    if finish == False:
        sprites_list = sprite.spritecollide(player, enemys, False)
        if sprites_list:
            won = font1.render('YOU LOSE', True, (255,215,0))
            finish = True
        sprite_list3 = sprite.spritecollide(player, asteroids, False)
        if sprite_list3:
            won = font1.render('YOU LOSE', True, (255,215,0))
            finish = True
        sprite_list2 = sprite.groupcollide(enemys, bulets, True, True)
        if sprite_list2:
            win += 1
            text_win = font1.render("Сбито:" + str(win), 1, (255,255,255))
            enemy = Enemy("grinch.png",randint(50,550),randint(-150,-60),1,(120,150))
            enemys.add(enemy)
        if win >= 15:
            won = font1.render('YOU WIN', True, (255,215,0))
            finish = True 
        if lost >= 15:
            won = font1.render('YOU LOSE', True, (255, 215,0))
            finish = True

        window.blit(text_lose,(10,10))
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_win,(10,56))
        player.reset()
        player.update()
        enemys.draw(window)
        enemys.update()
        bulets.draw(window)
        bulets.update()
        asteroids.draw(window)
        asteroids.update()
        