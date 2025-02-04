# импортируем зависимости и дополнительные модули
import pygame
from sys import exit
import time

# включаем модуль pygame
pygame.init()

# объявляем ширину и высоту экрана
width = 800
height = 400
# создаём экран игры
screen = pygame.display.set_mode((width, height))
# устанавливаем количество кадров в секунду
fps = 60
# создаём объект таймера
clock = pygame.time.Clock()

# добавляем счётчики для подсчёта времени в игре — это будут наши очки
start_time = 0
final_score = 0

# загружаем в переменные картинки из папки с нашим файлом
back_main_screen = pygame.image.load('code_game_back.jpg').convert()
back = pygame.image.load('code_game_back_floor.jpg').convert()
hero = pygame.image.load('detective.png').convert_alpha()
pot = pygame.image.load('teapot.png').convert_alpha()
candle = pygame.image.load('candlestick.png').convert_alpha()
box = pygame.image.load('wooden_box.png').convert_alpha()

# даём название окну игры
pygame.display.set_caption('Terraria mini Game')

# объявляем переменную-флаг для цикла игры
game = False

# создаём объекты текста
text_font = pygame.font.Font('prstartk.ttf', 15)
text_surface = text_font.render('TERRARIA MINI GAME', False, 'White')
text_name_rect = text_surface.get_rect(center=(400, 30))

text_font_collide = pygame.font.Font('prstartk.ttf', 50)
text_collide = text_font_collide.render('GAME OVER', False, 'Red')
text_collide_rect = text_collide.get_rect(center=(400, 200))

text_font_new_game = pygame.font.Font('prstartk.ttf', 20)
text_newgame_str1 = text_font_new_game.render('If you want to start,', False, 'White')
text_newgame_rect1 = text_newgame_str1.get_rect(center=(400, 325))
text_newgame_str2 = text_font_new_game.render('press space', False, 'White')
text_newgame_rect2 = text_newgame_str2.get_rect(center=(400, 350))

text_font_score = pygame.font.Font('prstartk.ttf', 15)
text_ts_font = pygame.font.Font('prstartk.ttf', 20)


# функция подсчёта очков
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = text_font_score.render(f'{current_time // 1000}', False, 'White')  # выводим время в секундах
    score_rect = score_surface.get_rect(bottomright=(795, 395))
    screen.blit(score_surface, score_rect)


# Функция для сброса начальных параметров
def reset_game():
    global hero_rect, pot_rect, candle_rect, box_rect, pot_flag, box_flag, game

    hero_x_pos = 75
    hero_y_pos = 180
    candle_x_pos = 900
    candle_y_pos = 70
    box_x_pos = 900
    box_y_pos = 200
    pot_x_pos = 900
    pot_y_pos = 345

    hero_rect = hero.get_rect(center=(hero_x_pos, hero_y_pos))
    pot_rect = pot.get_rect(center=(pot_x_pos, pot_y_pos))
    candle_rect = candle.get_rect(center=(candle_x_pos, candle_y_pos))
    box_rect = box.get_rect(center=(box_x_pos, box_y_pos))

    pot_flag = False
    box_flag = False


reset_game()

# запускаем бесконечный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not game and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()
            game = True
            start_time = pygame.time.get_ticks()

    if game:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            hero_rect.top -= 5
            if hero_rect.top <= 0:
                hero_rect.top = 0
        if keys[pygame.K_DOWN]:
            hero_rect.top += 5
            if hero_rect.bottom >= height:
                hero_rect.bottom = height

        screen.blit(back, (0, 0))
        screen.blit(hero, hero_rect)
        screen.blit(candle, candle_rect)
        screen.blit(box, box_rect)
        screen.blit(pot, pot_rect)
        screen.blit(text_surface, text_name_rect)  # исправлено: back на screen

        candle_rect.left -= 4
        if candle_rect.left <= 400:
            pot_flag = True
        if pot_flag:
            pot_rect.left -= 4
        if pot_rect.left <= 400:
            box_flag = True
        if box_flag:
            box_rect.left -= 4

        if candle_rect.right <= 0:
            candle_rect.left = 800
        if pot_rect.right <= 0:
            pot_rect.left = 800
        if box_rect.right <= 0:
            box_rect.left = 1000

        if hero_rect.colliderect(candle_rect) or hero_rect.colliderect(pot_rect) or hero_rect.colliderect(box_rect):
            screen.blit(text_collide, text_collide_rect)
            final_score = (pygame.time.get_ticks() - start_time) // 1000
            text_ts_text = text_ts_font.render(f'Total time: {final_score} sec', False, 'White')
            text_ts_rect = text_ts_text.get_rect(center=(400, 250))
            screen.blit(text_ts_text, text_ts_rect)
            pygame.display.flip()
            time.sleep(3)
            game = False

        display_score()

    else:
        screen.blit(back_main_screen, (0, 0))
        pygame.draw.rect(screen, 'Black', (100, 300, 600, 80))
        screen.blit(text_newgame_str1, text_newgame_rect1)
        screen.blit(text_newgame_str2, text_newgame_rect2)

    pygame.display.update()
    clock.tick(fps)