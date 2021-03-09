import pygame
import random
import time
import math
from tqdm import tqdm
import numpy as np

SCALE = 10
WHITE = (255, 255, 255)
SNAKE_COLOR = (255, 0, 0)
APPLE_COLOR = (0, 255, 0)
WIDTH = 50
HEIGHT = 50
BLACK = (0, 0, 0)


def display_snake(snake_position, display):
    for position in snake_position:
        pygame.draw.rect(
            display, SNAKE_COLOR, pygame.Rect(position[0], position[1], SCALE, SCALE),
        )


def display_apple(apple_position, display):
    pygame.draw.rect(
        display,
        APPLE_COLOR,
        pygame.Rect(apple_position[0], apple_position[1], SCALE, SCALE),
    )


def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))


def generate_snake(
    snake_start, snake_position, apple_position, button_direction, score
):
    if button_direction == 1:
        snake_start[0] += SCALE
    elif button_direction == 0:
        snake_start[0] -= SCALE
    elif button_direction == 2:
        snake_start[1] += SCALE
    else:
        snake_start[1] -= SCALE
    if snake_start == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_start))

    else:
        snake_position.insert(0, list(snake_start))
        snake_position.pop()

    return snake_position, apple_position, score


def collision_with_apple(apple_position, score):
    apple_position = [
        random.randrange(1, WIDTH) * SCALE,
        random.randrange(1, HEIGHT) * SCALE,
    ]
    score += 1
    return apple_position, score


def collision_with_boundaries(snake_start):
    if (
        snake_start[0] >= WIDTH * SCALE
        or snake_start[0] < 0
        or snake_start[1] >= HEIGHT * SCALE
        or snake_start[1] < 0
    ):
        return 1
    else:
        return 0


def collision_with_self(snake_start, snake_position):
    if snake_start in snake_position[1:]:
        return 1
    else:
        return 0


def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    left_direction_vector = np.array(
        [current_direction_vector[1], -current_direction_vector[0]]
    )
    right_direction_vector = np.array(
        [-current_direction_vector[1], current_direction_vector[0]]
    )

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked


def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    if (
        collision_with_boundaries(next_step) == 1
        or collision_with_self(next_step.tolist(), snake_position) == 1
    ):
        return 1
    else:
        return 0


def generate_random_direction(snake_position, angle_with_apple):
    direction = 0
    if angle_with_apple > 0:
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    else:
        direction = 0

    return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array(
        [current_direction_vector[1], -current_direction_vector[0]]
    )
    right_direction_vector = np.array(
        [-current_direction_vector[1], current_direction_vector[0]]
    )

    new_direction = current_direction_vector

    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction


def generate_button_direction(new_direction):
    button_direction = 0
    if new_direction.tolist() == [SCALE, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-SCALE, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, SCALE]:
        button_direction = 2
    else:
        button_direction = 3

    return button_direction


def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = SCALE
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = SCALE

    apple_direction_vector_normalized = (
        apple_direction_vector / norm_of_apple_direction_vector
    )
    snake_direction_vector_normalized = (
        snake_direction_vector / norm_of_snake_direction_vector
    )
    angle = (
        math.atan2(
            apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0]
            - apple_direction_vector_normalized[0]
            * snake_direction_vector_normalized[1],
            apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1]
            + apple_direction_vector_normalized[0]
            * snake_direction_vector_normalized[0],
        )
        / math.pi
    )
    return (
        angle,
        snake_direction_vector,
        apple_direction_vector_normalized,
        snake_direction_vector_normalized,
    )


def starting_positions():
    X, Y = (
        random.randrange(5, int(0.9 * WIDTH)) * SCALE,
        random.randrange(5, int(0.9 * HEIGHT)) * SCALE,
    )
    snake_start = [X, Y]
    snake_position = [[X - _offset * SCALE, Y] for _offset in range(0, 3)]
    apple_position = [
        random.randrange(1, WIDTH) * SCALE,
        random.randrange(1, HEIGHT) * SCALE,
    ]
    score = 3
    return snake_start, snake_position, apple_position, score


def play_game(
    snake_start,
    snake_position,
    apple_position,
    button_direction,
    score,
    display,
    clock,
    tick=50000,
):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill(WHITE)

        display_apple(apple_position, display)
        display_snake(snake_position, display)

        snake_position, apple_position, score = generate_snake(
            snake_start, snake_position, apple_position, button_direction, score
        )
        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()
        clock.tick(tick)

        return snake_position, apple_position, score
