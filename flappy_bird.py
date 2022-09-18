import pygame
import os
import random
import math
from screeninfo import get_monitors
pygame.mixer.init()
pygame.init()

FPS = 120

# WIDTH = [i.width for i in get_monitors()][-1]
# HEIGHT = [i.height for i in get_monitors()][-1]
WIDTH, HEIGHT = 1350, 760
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

flap_sound = pygame.mixer.Sound(os.path.join("Assets", "wing.mp3"))
flap_sound.set_volume(0.1)
die_sound = pygame.mixer.Sound(os.path.join("Assets", "die.mp3"))
die_sound.set_volume(0.1)
hit_sound = pygame.mixer.Sound(os.path.join("Assets", "hit.mp3"))
hit_sound.set_volume(0.1)
swoosh_sound = pygame.mixer.Sound(os.path.join("Assets", "swoosh.mp3"))
swoosh_sound.set_volume(0.1)
point_sound = pygame.mixer.Sound(os.path.join("Assets", "point.mp3"))
point_sound.set_volume(0.05)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BIRD_HEIGHT = HEIGHT // 9
BIRD_WIDTH = BIRD_HEIGHT // 1.45
BIRD = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "birdie.png")), (BIRD_HEIGHT, BIRD_WIDTH)).convert_alpha()
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "flappy_backround.png")), (WIDTH, HEIGHT)).convert_alpha()
GAME_OVER = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "game_over.jpg")), (WIDTH, HEIGHT)).convert_alpha()
PIPE_WIDTH, PIPE_HEIGHT = WIDTH//8.5, WIDTH//3
PIPE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "pipe.png")), (PIPE_WIDTH, PIPE_HEIGHT)).convert_alpha()
UPSIDE_DOWN_PIPE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "upside_down_pipe.png")), (PIPE_WIDTH, PIPE_HEIGHT)).convert_alpha()
RESTART_WIDTH, RESTART_HEIGHT = HEIGHT//7 * 2.8, HEIGHT//7
RESTART = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "restart.png")), (RESTART_WIDTH, RESTART_HEIGHT)).convert_alpha()
WHITE_SQUARE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "white.png")), (WIDTH*2, HEIGHT*2)).convert_alpha()

WHITE_SQUARE.set_alpha(135)

jump_height = HEIGHT/127
gravity = 0.2
pipe_distance = [300]


def draw_window(bird, BIRD, bird_rotation, score_text, score_text_rect, dead, pipes, high_score_number, high_score_number_rect, high_score_text, high_score_text_rect, high_score, score):
    WIN.blit(BACKGROUND, (0, 0))
    BIRD = pygame.transform.rotate(BIRD, bird_rotation[0])
    WIN.blit(BIRD, bird)

    for pipe in pipes["lower_pipes"]:
        WIN.blit(PIPE, pipe)
    for pipe in pipes["upper_pipes"]:
        WIN.blit(UPSIDE_DOWN_PIPE, pipe)

    WIN.blit(score_text, score_text_rect)
    if high_score[0] == score[0] and not dead[0]:
        WIN.blit(high_score_text, high_score_text_rect)

    if dead[0]:
        WIN.blit(WHITE_SQUARE, (-WIDTH//2, -HEIGHT//2))
        WIN.blit(RESTART, (WIDTH / 2 - RESTART_WIDTH / 2, HEIGHT / 1.5 - RESTART_HEIGHT / 2))
        WIN.blit(high_score_number, high_score_number_rect)

    pygame.display.update()


def bird_movement(bird, flap, bird_acceleration, bird_rotation):
    bird.y -= bird_acceleration[0]
    bird_acceleration[0] -= gravity
    if bird_acceleration[0] < -22:
        bird_acceleration[0] = -22
    if flap:
        bird_acceleration[0] = jump_height
        flap_sound.play()

    bird_rotation[0] = bird_acceleration[0] * 6
    if bird_rotation[0] < -75:
        bird_rotation[0] = -75
    if bird_rotation[0] > 50:
        bird_rotation[0] = 50

    if bird.y + BIRD.get_height() > HEIGHT - BIRD.get_height()/3:
        bird.y = HEIGHT - BIRD.get_height() - BIRD.get_height()/3
    if bird.y < 0 - BIRD.get_height()/3:
        bird.y = 0 - BIRD.get_height()/3
        bird_acceleration[0] = 0


def pipe_controller(pipes, bird, dead, score, high_score):
    if not dead[0]:
        random_y = random.randrange(int((HEIGHT/5)*2.75), int((HEIGHT/5)*4.25))
        if len(pipes["lower_pipes"]) == 0:
            pipes["lower_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["upper_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y - pipe_distance[0] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["pipe_barriers"].append(pygame.Rect(WIDTH + PIPE_WIDTH*2, random_y - pipe_distance[0], 2.5, pipe_distance[0]))
        elif len(pipes["lower_pipes"]) == 1 and pipes["lower_pipes"][0].x <= (WIDTH//4)*3:
            pipes["lower_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["upper_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y - pipe_distance[0] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["pipe_barriers"].append(pygame.Rect(WIDTH + PIPE_WIDTH*2, random_y - pipe_distance[0], 2.5, pipe_distance[0]))
        elif len(pipes["lower_pipes"]) == 2 and pipes["lower_pipes"][1].x <= (WIDTH//4)*3:
            pipes["lower_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["upper_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y - pipe_distance[0] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["pipe_barriers"].append(pygame.Rect(WIDTH + PIPE_WIDTH*2, random_y - pipe_distance[0], 2.5, pipe_distance[0]))
        elif len(pipes["lower_pipes"]) == 3 and pipes["lower_pipes"][2].x <= (WIDTH//4)*3:
            pipes["lower_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["upper_pipes"].append(pygame.Rect(WIDTH + PIPE_WIDTH, random_y - pipe_distance[0] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT))
            pipes["pipe_barriers"].append(pygame.Rect(WIDTH + PIPE_WIDTH*2, random_y - pipe_distance[0], 2.5, pipe_distance[0]))
        for pipe in pipes["lower_pipes"]:
            if pipe.x + PIPE_WIDTH <= 0:
                pipes["lower_pipes"].remove(pipe)
            pipe.x -= 3
            if pygame.Rect.colliderect(bird, pipe):
                dead[0] = True
        for pipe in pipes["upper_pipes"]:
            if pipe.x + PIPE_WIDTH <= 0:
                pipes["upper_pipes"].remove(pipe)
            pipe.x -= 3
            if pygame.Rect.colliderect(bird, pipe):
                dead[0] = True
        for pipe in pipes["pipe_barriers"]:
            if pipe.x + PIPE_WIDTH <= 0:
                pipes["pipe_barriers"].remove(pipe)
            pipe.x -= 3
            if 1.25 >= bird.x - pipe.x >= - 1.25:
                score[0] += 1
                if score[0] > high_score[0]:
                    high_score[0] = score[0]
                point_sound.play()
        pipe_distance[0] -= 0.03
        # if pipe_distance[0] < 90 + BIRD_HEIGHT + math.sqrt(BIRD_HEIGHT + BIRD_WIDTH):
        #     pipe_distance[0] = 300
        if score[0] % 20 == 0:
            pipe_distance[0] = 300


def main():
    bird = BIRD.get_rect().move(int(WIDTH * 0.25 - BIRD_WIDTH / 2), HEIGHT // 2)
    clock = pygame.time.Clock()
    second = 0

    bird_acceleration = [0]
    bird_rotation = [0]
    score = [0]
    high_score = [0]

    pipes = {"lower_pipes": [], "upper_pipes": [], "pipe_barriers": []}

    score_font = pygame.font.Font("freesansbold.ttf", 100)
    high_score_font = pygame.font.Font("freesansbold.ttf", 300)
    high_score_text_font = pygame.font.Font("freesansbold.ttf", 50)

    dead = [False]

    while True:
        clock.tick(FPS)  # Caps framerate
        second += 1 / FPS  # Keeps track of time
        flap = False
        score_text = score_font.render(str(score[0]), True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topright = (WIDTH - 10, 10)

        high_score_number = high_score_font.render(f"{high_score[0]}", True, YELLOW)
        high_score_number_rect = (WIDTH//2 - high_score_number.get_width()//2, HEIGHT//3.5 - high_score_number.get_height()//2)

        high_score_text = high_score_text_font.render("HIGH SCORE", True, YELLOW)
        high_score_text_rect = (WIDTH // 2 - high_score_text.get_width() // 2, 20)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if bird.y + BIRD.get_height() >= HEIGHT - BIRD.get_height()/3:
            dead = [True]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit


            if pygame.mouse.get_pressed()[0] and not dead[0]:
                flap = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dead[0]:
                    flap = True

        if not dead[0]:
            bird_movement(bird, flap, bird_acceleration, bird_rotation)
            pipe_controller(pipes, bird, dead, score, high_score)

        if dead[0]:
            bird_acceleration[0] = 0

        if dead[0] and pygame.mouse.get_pressed()[0] and WIDTH / 2 - RESTART_WIDTH / 2 < mouse_x < WIDTH / 2 + RESTART_WIDTH / 2 \
            and HEIGHT / 1.5 - RESTART_HEIGHT / 2 < mouse_y < HEIGHT / 1.5 + RESTART_HEIGHT / 2:
            bird.y = HEIGHT // 2
            score[0] = 0
            bird_acceleration[0] = jump_height
            pipes = {"lower_pipes": [], "upper_pipes": [], "pipe_barriers": []}
            pipe_distance[0] = 300
            dead[0] = False

        draw_window(bird, BIRD, bird_rotation, score_text, score_text_rect, dead, pipes, high_score_number,
                    high_score_number_rect, high_score_text, high_score_text_rect, high_score, score)


if __name__ == "__main__":
    main()
