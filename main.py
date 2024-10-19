from typing import Any
import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height, points):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.points = points
        
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
            if self.rect.y > 550:
                self.rect.y = 550
                
    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
            if self.rect.y > 550:
                self.rect.y = 550

#Игровая сцена:            
img_back = 'galaxy.png'
img_asteroid = 'asteroid.png'
img_racket = 'racket.png'

back = (200, 255, 255)
win_width = 1200
win_height = 700
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))

pygame.font.init()
font1 = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 36)
lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))

#Фоновая музыка:
pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()

#Флаги отвечающие за состояние игры
game = True
finish = False
game_over = False
clock = pygame.time.Clock()
FPS = 60

#Создание мяча и ракетки
racket1 = Player(img_racket, 30, 200, 4, 50, 150, 0)
racket2 = Player(img_racket, 1120, 200, 4, 50, 150, 0)
ball = GameSprite(img_asteroid, 200, 200, 4, 50, 50)

speed_x = 2
speed_y = 2

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            
    if finish != True:
        score = font2.render("Счет: " + str(racket1.points) + ' : ' + str(racket2.points), 1, (255, 255, 255))
        window.blit(score, (500, 20))
        window.blit(background, (0, 0))
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        
        if pygame.sprite.collide_rect(racket1, ball) or pygame.sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1
            
        if ball.rect.x < 0:
            racket1.points += 1
            if racket1.points > 5:
                finish = True
                window,blit(lose1, (200, 200))
                
        if ball.rect.x > win_width:
            racket2.points += 1
            if racket2.points > 5:
                finish = True
                window.blit(lose2, (200, 200))
                
        racket1.reset()
        racket2.reset()
        ball.reset()
    
    pygame.display.update()
    clock.tick(FPS)
        