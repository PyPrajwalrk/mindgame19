import pygame
import random
import sys
import time

# Initialize Pygame & Sound System
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mind Architect - Star Quest")

# Colors
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 250)
HOVER_COLOR = (100, 200, 250)
GOLD_COLOR = (255, 215, 0)

# Font
FONT = pygame.font.SysFont("Arial", 36)
SMALL_FONT = pygame.font.SysFont("Arial", 28)

# Game variables
level = 1
score = 0
total_stars = 0
max_level = 15

# Load Sound Effects
win_sound = pygame.mixer.Sound("win_sound.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, w, h, normal_color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    
    if rect.collidepoint(mouse):
        pygame.draw.rect(SCREEN, hover_color, rect, border_radius=10)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(SCREEN, normal_color, rect, border_radius=10)
    
    draw_text(text, SMALL_FONT, TEXT_COLOR, SCREEN, x + w // 2, y + h // 2)
    return False

def generate_puzzle(level):
    """ Generates a puzzle based on the level """
    return [random.randint(1, 9) for _ in range(level + 2)]

def play_puzzle(puzzle):
    global score, level, total_stars

    SCREEN.fill(BACKGROUND_COLOR)
    draw_text("Memorize the Numbers!", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 3)
    pygame.display.flip()
    time.sleep(2)
    SCREEN.fill(BACKGROUND_COLOR)

    # Display puzzle elements
    for number in puzzle:
        draw_text(str(number), FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(0.8)
        SCREEN.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        time.sleep(0.2)

    user_input = ""
    start_time = time.time()

    while True:
        SCREEN.fill(BACKGROUND_COLOR)
        draw_text(f"Enter the sequence (Level {level})", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)
        draw_text(user_input, FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == ''.join(map(str, puzzle)):
                        pygame.mixer.Sound.play(win_sound)
                        end_time = time.time()
                        elapsed_time = end_time - start_time

                        # Calculate stars
                        if elapsed_time <= 3:
                            stars = 3
                        elif elapsed_time <= 5:
                            stars = 2
                        else:
                            stars = 1

                        score += 10 * level * stars
                        total_stars += stars
                        level += 1
                        return True
                    else:
                        pygame.mixer.Sound.play(lose_sound)
                        return False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

# Main game loop
while True:
    if level > max_level:
        SCREEN.fill(BACKGROUND_COLOR)
        draw_text("🎉 Congratulations! You Completed Mind Architect - Star Quest! 🎉", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(f"Your Score: {score}", SMALL_FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        draw_text(f"Total Stars Earned: {total_stars} / {max_level * 3}", SMALL_FONT, GOLD_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()
        pygame.time.wait(5000)
        break
    
    SCREEN.fill(BACKGROUND_COLOR)
    draw_text(f"Level: {level}", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Score: {score}", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4 + 50)
    draw_text(f"Total Stars: {total_stars}", FONT, GOLD_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4 + 100)

    if draw_button("Start Puzzle", WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60, BUTTON_COLOR, HOVER_COLOR):
        puzzle = generate_puzzle(level)
        play_puzzle(puzzle)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
