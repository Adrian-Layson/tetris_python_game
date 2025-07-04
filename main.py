import pygame, sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

left_pressed = False
right_pressed = False
move_delay = 100
last_move_time = 0

while True:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
                
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()
                left_pressed = True
                right_pressed = False
                last_move_time = current_time
                
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()
                right_pressed = True
                left_pressed = False
                last_move_time = current_time
                
            if event.key == pygame.K_DOWN and not game.game_over:
                if game.move_down():
                    game.update_score(0, 1)
                
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()
                
            if event.key == pygame.K_SPACE and not game.game_over:
                game.hard_drop()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_RIGHT:
                right_pressed = False
                
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    if not game.game_over:
        if left_pressed and current_time - last_move_time > move_delay:
            if game.move_left():
                last_move_time = current_time
            else:
                left_pressed = False
                
        if right_pressed and current_time - last_move_time > move_delay:
            if game.move_right():
                last_move_time = current_time
            else:
                right_pressed = False

    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(
        centerx=score_rect.centerx, 
        centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)