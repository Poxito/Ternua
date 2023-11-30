import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ternua")

# Load background images - TO BE DONE
#green_image = pygame.image.load("green_image.png")
#blue_image = pygame.image.load("blue_image.png")

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
darkgreen = (0, 102, 0)
seablue = (36, 122, 207)

score = 0
high_scores = []

def display_high_scores():
    screen.fill((0, 0, 0))  # Fill the entire screen with black

    text = font.render("High Scores", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, 50))
    screen.blit(text, text_rect)

    y = 100
    for idx, score_value in enumerate(high_scores, start=1):
        score_text = score_font.render(f"{idx}. {score_value}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, y))
        screen.blit(score_text, score_rect)
        y += 40

    restart_text = font.render("Press 'R' to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(width // 2, height - 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

font = pygame.font.Font(None, 36) # I have to change the font
score_font = pygame.font.Font(None, 36) # I have to change the font
restart_font = pygame.font.Font(None, 36) # I have to change the font

def starting_screen():
    screen.fill((0, 0, 0))
    text = font.render("Press ENTER to start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    pygame.display.update(text_rect)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def reset_game():
    enemy_rect.x = random.randint(0, width - enemy_rect.width)
    enemy_rect.y = height
    enemy_speed = 2
    player_speed = 5
    bullet_speed = 3

def display_score():
    score_text = score_font.render(f"1: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topleft=(10, 10))
    screen.blit(score_text, score_rect)

player_image = pygame.image.load("arrantzalea.png")
player_rect = player_image.get_rect()
player_rect.center = (width // 2, 30)
player_speed = 5

enemy_image = pygame.image.load("arraina.png")
enemy_rect = enemy_image.get_rect()
enemy_speed = 2
reset_game()

bullet_image = pygame.image.load("sarea.png")
bullet_rect = bullet_image.get_rect()
bullet_speed = 3
bullet = None
bullet_cooldown = 0 

clock = pygame.time.Clock()

in_starting_screen = True
game_over = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_starting_screen and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            in_starting_screen = False

        if (game_over or in_starting_screen) and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            in_starting_screen = True

    if in_starting_screen:
        starting_screen()
        in_starting_screen = False 
        game_over = False 
        score = 0

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < width:
            player_rect.x += player_speed

        if keys[pygame.K_SPACE] and bullet_cooldown == 0:
            bullet = bullet_image.get_rect(midtop=(player_rect.centerx, player_rect.top)) #pygame.Rect(player_rect.centerx - 2, player_rect.top, 5, 10)
            bullet_cooldown = 10

        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        if bullet:
            bullet.y += bullet_speed
            if bullet.bottom >= height:
                bullet = None

        if bullet and bullet.colliderect(enemy_rect):
            score += 1
            bullet = None
            enemy_rect.x = random.randint(0, width - enemy_rect.width)
            enemy_rect.y = height
        
        if score >= 10 and enemy_speed == 2:
            enemy_speed += 1

        if score >= 50 and enemy_speed == 3:
            enemy_speed += 1 

        if score >= 100 and enemy_speed == 4:
            enemy_speed += 1
            player_speed += 1
            bullet_speed += 1
        
        enemy_rect.y -= enemy_speed
        if enemy_rect.y <= 64:
            high_scores.append("  1:" + str(score))
            high_scores.sort(reverse=True)
            high_scores = high_scores[:5]
            game_over = True

        screen.fill(darkgreen, (0, 0, width, 65))
        screen.fill(seablue, (0, 65, width, height))

        screen.blit(player_image, player_rect)
        screen.blit(enemy_image, enemy_rect)
        if bullet:
            screen.blit(bullet_image, bullet)

        display_score()

        if game_over:
            display_high_scores()
            reset_game()

        clock.tick(60)
        
    pygame.display.update()

pygame.quit()
sys.exit()