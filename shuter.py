# -------- GALADEB V0.1 ----------
# --------- by Xoce --------------

from pygame import *
from random import randint, choice
from generate_shoots import yes_or_no
import time
from pygame.locals import *
import pygame




font.init()
mixer.init()
font = font.Font(None, 36)


img_menu = 'sprites/start_back1.jpg'
img_back = 'sprites/galaxy.png'
img_hero_ship = 'sprites/ship3.png'
img_gameover = 'sprites/gameover1.png'
img_win = 'sprites/win1.png'
img_blast = 'sprites/blust.png'
img_bullet = 'sprites/bullet.png'
img_enemy = 'sprites/ship4.png'
img_enemy_bullet = 'sprites/bullet_enemy.png'
img_boss_enemy = 'sprites/ship6.png'
img_heart = 'sprites/heart.png'
img_ship = 'sprites/ship4.png'
img_start_but = 'sprites/start_but.png'
img_repeat_but = 'sprites/repeat_but.png'
img_quit_but = 'sprites/quit_but.png'
img_boom = 'sprites/boom.png'
# img_about_but = 'about_but.png'


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)


        self.image = transform.scale(image.load(player_image).convert_alpha(), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
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
        bullet = Bullet(img_bullet, self.rect.right-20, self.rect.top, 15, 20, 15)
        bullet2 = Bullet(img_bullet, self.rect.left+5, self.rect.top, 15, 20, 15)
        bullet3 = Bullet(img_bullet, self.rect.centerx-8, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        bullets.add(bullet2)
        bullets.add(bullet3)
    
    # def fire_bluster(self):
    #     top = self.rect.top-500
    #     center = self.rect.centerx-5
    #     # center = self.rect.x + 35
    #     blust = Bluster(img_blast, center, top, 10, 600, 0)
        
    #     # blust = Bullet(img_bullet, self.rect.centerx, self.rect.top, 60, 200, 15)
    #     blusters.add(blust)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            global lost
            lost = lost + 1


class EnemyBoss(GameSprite):
    move = 'right'
    left_side = 200
    right_side = 700
    def update(self):
        if self.rect.x <= self.left_side: 
            self.move = 'right'
        if self.rect.x <= self.left_side:
            self.left_side = randint(200, win_width/2)
        if self.rect.x >= self.right_side:
            self.move = 'left'
        if self.rect.x >= self.right_side:
            self.right_side = randint(501, win_width) - 200
        if self.move == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def update_for_scene(self):
        if self.rect.y < 0: # если координата меньше 0, а по дефолту она ширина экрана - 300
            self.rect.y += 2 # то увеличиваем движение/координату корабля
        if self.rect.y >= 120: # если она достигла 
            self.rect.y = 0

        
    def fire(self):
        bullet = BulletEnemys(img_enemy_bullet, self.rect.right-7, self.rect.bottom-150, 3, 13, 15)
        bullet1 = BulletEnemys(img_enemy_bullet, self.rect.left+4, self.rect.bottom-150, 3, 13, 15)
        bullet2 = BulletEnemys(img_enemy_bullet, self.rect.centerx-1, self.rect.top+185, 3, 13, 15)
        bullets_enemy.add(bullet)
        bullets_enemy.add(bullet1)
        bullets_enemy.add(bullet2)

    
    def change_skin(self, filename):
        self.image = transform.scale(image.load(filename).convert_alpha(), (200, 220))
        

       
class BulletEnemys(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


'''
При получении координат клика мыши мы проверяем их, попали ли они в нужный пряумольник/sprite/текст
если координата мыши больше чем начальная точка спрайта Х (слева вверхний угол) AND меньше чем конечная точка Х. 
Как вычислить конечную точку? 
начальная точка Х (левый вверхних угол) + размер спрайта = конец точки спрайта
'''
class Buttons(GameSprite):
    def click_button_repeat(self, pos):
        mouse_x, mouse_y = pos 
        if (mouse_x > self.rect.x and mouse_x < self.rect.x + 233) and (mouse_y > self.rect.y and mouse_y < self.rect.y + 50):
            return True
    
    def click_button_quit(self, pos):
        mouse_x, mouse_y = pos 
        if (mouse_x > self.rect.x and mouse_x < self.rect.x + 180) and (mouse_y > self.rect.y and mouse_y < self.rect.y + 50):
            return True

    def click_button_start(self, pos):
        mouse_x, mouse_y = pos
        if (mouse_x > self.rect.x and mouse_x < self.rect.x + 233) and (mouse_y > self.rect.y and mouse_y < self.rect.y + 50):
            return True


# class Bluster(GameSprite):
#     def update(self):
#         if self.rect.y < 0:
#             self.kill()


# флаг для оптимизации
flags = DOUBLEBUF | pygame.FULLSCREEN | pygame.HWACCEL 
# ---- возможно придется опустить до нуля ширину и высоту ----
win_width = 1024 #1024 
win_height = 720 #720
# ---- возможно придется опустить до нуля ширину и высоту ----
display.set_caption('Space War')
window = display.set_mode((win_width, win_height), flags)
window.set_alpha(None)
size_info = display.Info() # получаем актуальные размеры экрана
win_width = size_info.current_w # и передаем переменным
win_height = size_info.current_h 
window = display.set_mode((win_width, win_height), flags) # подставляем вместе с флагами оптимизации и фуллэкрана


background = transform.scale(image.load(img_back).convert(), (win_width, win_height))
shoot_sound = mixer.Sound('sounds/bullet.mp3')
shoot_bluster_sound = mixer.Sound('sounds/bluster.mp3')
back_music = mixer.Sound('sounds/back_music.mp3')
boom = mixer.Sound('sounds/boom.wav')
menu_music = mixer.Sound('sounds/menu.mp3')
win_music = mixer.Sound('sounds/win.mp3')
gameover_voice = mixer.Sound('sounds/gameover1.mp3')
menu_music.play(loops=1)
# boss_enemy_music = mixer.Sound('sounds/boss_music.mp3')
 


bullets = sprite.Group()
bullets_enemy = sprite.Group()
enemys = sprite.Group()
# blusters = sprite.Group()


# about_but = Buttons(img_about_but, win_width/3+50, win_height/1, 233, 50, 0)
start_but = Buttons(img_start_but, win_width/3+50, win_height/2, 233, 50, 0)
repeat_but = Buttons(img_repeat_but, win_width/3+50, win_height/2, 233, 50, 0)
quit_but = Buttons(img_quit_but, win_width/3+75, win_height/2+60, 180, 50, 0)
ship_icon = GameSprite(img_ship, 188, 40, 30, 30, 0)
heart_icon = GameSprite(img_heart, 275, 71, 40, 40, 0)
ship = Player(img_hero_ship, 5, win_height - 120, 80, 100, 10)
enemy_boss = EnemyBoss(img_boss_enemy, 410, -300, 200, 200, 5) #Y -300
for i in range(1, 6):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 70, randint(1, 5))
    enemys.add(enemy)




score = 0
lost = 0
ship_health = 3
boss_ship_hp = 10000
finish = False # вернуть на False
blust_fire = False
run = True
cat_scene = True
shift = 0
count_clear_bullets = 0
lose = False
menu = True
interval_fire = 0

while run:
    if not menu:
        menu_music.stop()
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE and not lose:
                # and blust_fire == False:
                    if time.time() - interval_fire > 0.5: # ограничение на скорость выпуска пуль
                        ship.fire()
                        shoot_sound.play()
                        interval_fire = time.time()
            elif e.type == MOUSEBUTTONDOWN and lose: # если игра окончена и нажата кнопка мыши
                if repeat_but.click_button_repeat(mouse.get_pos()): # а именно на позицию REPEAT(sprite), то мы отправляем коор. мыши в нашу функцию
                    ship_health, score, lost, boss_ship_hp, enemy_boss.rect.y, lose = 3, 0, 0, 10000, -300, False # обнуляем и дополняем исходные показатели
                    enemys.empty() # очищаем группы с врагами, пулями и пулями врага
                    bullets_enemy.empty()
                    bullets.empty()
                    win_music.stop() # < --- останавливаем победный сауд
                    for i in range(1, 6): # заново заполняем список с юнитами/врагами
                        enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                        enemys.add(enemy)
                    back_music.play(loops=-1)
                    finish = False # возвращаемся в игру
                    
            
                if quit_but.click_button_quit(mouse.get_pos()): # если клик был на sprite выхода, то
                    run = False # останавливаем цикл игры

            # ----------- бластер [в заморозке] --------------
                # if e.key == K_a:
                    # blust_fire = True
            # elif e.type == KEYUP:
                # if e.key == K_a:
                    # blust_fire = False
        

        # if blust_fire:
            # ship.fire_bluster()
            # shoot_bluster_sound.play()
            # window.blit(background, (0, 0))

            # -------------------------------------------------
        
        # if boom is None:
            # window.blit(transform.scale(image.load(img_gameover), (win_width, win_height)), (0, 0))
        if not finish:
            # window.blit(background.convert(), (0, 0))
            shift -= 5
            local_shift = shift % win_height
            window.blit(background.convert(), (0, local_shift)) 
            if local_shift != 0:
                window.blit(background.convert(), (0, local_shift - win_height))
            
            # пишем текст на экране
            text = font.render("Счет: " + str(score), 1, (255, 255, 255))   
            window.blit(text, (10, 20))
        
            text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))


            
            ship_icon.reset()
            # repeat_but.reset()
            # quit_but.reset()
            # ramka.reset()
            
            # желаемое кол-во врагов * 8 = нужное количество очков для достижения
            if score <= 1200: # если кол-во убитых врагов/очков меньше чем это число, то босс пока не вызывается *сейчас это 150 врагов* 
                ship.update()
                ship.reset()
                bullets.draw(window) # отрисовка патронов нашего корабля
                bullets.update()
                enemys.draw(window)
                enemys.update()

                # blusters.draw(window)
                
                # при столкновении врагов с кораблем, выводится текст GAMEOVER
                if sprite.spritecollide(ship, enemys, False) or lost >= 3:
                    finish = True
                    lose = True
                    gameover_voice.play()
                    # d = img.get_width() // img.get_height()
                    # window.fill((255,255,255))
                    window.blit(transform.scale(image.load(img_gameover), (win_width, win_height)), (0, 0))
                    repeat_but.reset() # кнопка перезапуска игры
                    quit_but.reset()
                    back_music.stop()
                    
                    


            # <--------------------- Здесь про стандартных юнитов ---------------------- >
            # при столкновении врагов с пулями, враги удаляются и их место занимают другие
                colides = sprite.groupcollide(enemys, bullets, True, True)
                for c in colides:
                    score = score + 8 # за 1 убитого врага дают 8 очков
                    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                    enemys.add(enemy)


            else: # вернуть потом на else
            # <----------------------- Здесь про главного босса -------------------------->
                # back_music = mixer.Sound('boss_music.mp3')
                text_health = font.render("Количество жизней: " + str(ship_health), 1, (255, 255, 255))
                window.blit(text_health, (10, 80))

                text_enemy_boss_hp = font.render("Прочность корабля: " + str(boss_ship_hp) + '/10000', 1, (255, 255, 255))
                window.blit(text_enemy_boss_hp, (10, 110))

                heart_icon.reset()
                enemy_boss.change_skin(img_boss_enemy)
                # Данный блок кода отвечает за кат-сцену, плавный прилет корабля босса
                if enemy_boss.rect.y != 0: # если координата корабля босса не равна нулю, то значит он не в позиции для стрельбы
                    enemy_boss.update_for_scene() # и поэтому мы вызываем плавное движение благодаря созданной функции
                    enemy_boss.reset() # и конечно же обновляем состояние корабля/картинки
                    shoot_sound.stop() 
                    
                else: # в update_for_scene я задал новую координату У = 0 и поэтому мы вызываем уже другое движение
                    enemy_boss.update()
                    enemy_boss.reset()
                    ship.update()
                    bullets_enemy.draw(window)
                    bullets_enemy.update()
                    bullets.update()
                    bullets.draw(window) # отрисовка патронов нашего корабля
                    
                ship.reset()
            
                
                
                # при столкновении пуль босса с кораблем больще чем на 3 выстрела, то игра заканчивается
                # print(sprite.spritecollide(ship, bullets_enemy, False))
                if sprite.spritecollide(ship, bullets_enemy, True):
                    ship_health -= 1
                    if ship_health <= 0:
                        finish = True
                        lose = True
                        gameover_voice.play()
                        # d = img.get_width() // img.get_height()
                        # window.fill((255,255,255))
                        window.blit(transform.scale(image.load(img_gameover), (win_width, win_height)), (0, 0))
                        back_music.stop()
                        repeat_but.reset() # кнопка перезапуска игры
                        quit_but.reset()
                # при столкновении с кораблем босса пуль нашего корабля, то идет минус прочности брони корабля
                if sprite.spritecollide(enemy_boss, bullets, True):
                    boss_ship_hp -= randint(30, 150)
                    score += 20
                    count = 0
                    if boss_ship_hp <= 0:
                        enemy_boss.change_skin(img_boom)
                        boom.play()
                        enemy_boss.reset() # < --- и это тоже обновляет, но конкретно корабль
                        display.update() # < --- дает обновиться кораблю взрывом, тк обновляет весь экран/игру
                        back_music.stop()
                        win_music.play(loops=1)
                        time.sleep(3)
                        window.blit(transform.scale(image.load(img_win), (win_width, win_height)), (0, 0))
                        finish = True
                        lose = True
                        repeat_but.reset() # кнопка перезапуска игры
                        quit_but.reset()
                # алгоритм который генерирует 300 вариантов нет не выстрелить и 50 вариантов - да
                # если всех вариантов choice выберит YES, то выстрелам быть.
        
                shoots = yes_or_no()
                result_shoot = choice(shoots)
                # clear_bullets_enemy = list()
                if result_shoot == 'yes':
                    enemy_boss.fire()
                #     print(bullets_enemy)
                # if result_shoot == 'no' and len(bullets_enemy) >= 30:
                #     bullets_enemy.empty()

                
    else:
        window.blit(transform.scale(image.load(img_menu), (win_width, win_height)), (0, 0))
        start_but.reset()
        quit_but.reset()
        # about_but.reset()
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN and menu: # если игра не начата и нажата кнопка
                if repeat_but.click_button_start(mouse.get_pos()):
                    back_music.play(loops=-1)
                    menu = False
                if quit_but.click_button_quit(mouse.get_pos()): # если клик был на sprite выхода, то
                    run = False # останавливаем цикл игры
            
        
        
    display.update()
    pygame.time.delay(35)
    