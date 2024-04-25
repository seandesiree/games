import pygame  
import random  

pygame.init()

# Set up the screen
screen_width, screen_height = 640, 480  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("TwinPicnic")  

# Load and scale images for player and enemy
player_image_original = pygame.transform.scale(pygame.image.load('./assets/Alisa-1.jpg'), (125, 115))
enemy_image = pygame.transform.scale(pygame.image.load('./assets/HAFSAOF-1.jpg'), (50, 50))

# Player setup
player_size = player_image_original.get_size()  
player_pos = [screen_width // 2, screen_height - player_size[1]]  
player_image = player_image_original.copy()  
facing_right = False  

# Enemy setup
enemy_size = enemy_image.get_size()  
enemy_pos = [random.randint(0, screen_width - enemy_size[0]), 0]  
enemy_speed = 5  

# Game loop
clock = pygame.time.Clock()  
game_over = False  

# To make the game pregessively harder start a speed_clock to track game time
speed_clock=0

while not game_over:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            game_over = True

    # Increase enemy speed as the game progresses to increase difficulty 
    if speed_clock%50==0:
        enemy_speed += 1

    # Player movement
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_LEFT]: 
        player_pos[0] -= 10  
        if facing_right:  
            player_image = pygame.transform.flip(player_image, True, False)  
            facing_right = False  
    elif keys[pygame.K_RIGHT]: 
        player_pos[0] += 10 
        if not facing_right: 
            player_image = pygame.transform.flip(player_image, True, False)  
            facing_right = True  

    # Ensure player remains within screen bounds
    player_pos[0] = max(0, min(player_pos[0], screen_width - player_size[0]))

    # Update enemy position
    enemy_pos[1] += enemy_speed  
    if enemy_pos[1] > screen_height:  
        enemy_pos = [random.randint(0, screen_width - enemy_size[0]), -enemy_size[1]]  

    # Collision detection
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])  
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1])  
    if player_rect.colliderect(enemy_rect):  
        game_over = True  

    # Draw elements
    screen.fill((0, 0, 0))  
    screen.blit(player_image, (player_pos[0], player_pos[1]))  
    screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1])) 
    pygame.display.update()  
    
    # Increment the speed_clock by 1
    speed_clock+=1

    # Cap the frame rate
    clock.tick(30)  


pygame.quit()