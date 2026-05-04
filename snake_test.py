#from snake import io_handler
#from snake_ref import io_handler
import snake_pygame_fixed

import pytest
import pygame

pygame.init()
pygame.display.set_mode((1,1))

snake = snake_pygame_fixed

side = snake.side_len

def test_mov():
    g = snake.game((640, 640))

    g.snake.head_x = 0
    g.snake.head_y = 0
    g.snake.body = [(0, 0)]

    g.last_input = 'd'
    g.movement()

    assert ((g.snake.head_x // side) , (g.snake.head_y // side)) == (1, 0)
    assert ((g.snake.body[0][0] // side), (g.snake.body[0][1] // side)) == (0, 0)

    g.movement()
    assert ((g.snake.head_x // side), (g.snake.head_y // side)) == (2, 0)

@pytest.mark.parametrize("x_before, y_before, x_after, y_after, key", [
    (0, 0, 0, 9, 'w'),
    (0, 0, 9, 0, 'a'),
    (9, 9, 9, 0, 's'),
    (9, 9, 0, 9, 'd'),
])

def test_boundaries(x_before, y_before, x_after, y_after, key):
    g = snake.game((10*side, 10*side))

    g.prev_input = key

    g.snake.head_x = x_before * side
    g.snake.head_y = y_before * side

    g.last_input = key
    g.movement()

    assert ((g.snake.head_x // side), (g.snake.head_y // side)) == (x_after, y_after)


def test_eat_fruit():
    g = snake.game((640, 640))

    g.snake.head_x = 0
    g.snake.head_y = 0

    g.snake.head_hitbox.x = 0
    g.snake.head_hitbox.y = 0

    fruit = pygame.Rect(side, 0, side, side)
    g.fruit_hitboxes.append(fruit)

    g.last_input = 'd'
    g.movement()

    assert g.snake.size == 3
    checker = pygame.Rect(side, 0, side, side)
    for k in range(len(g.fruit_hitboxes)):
        assert (checker.colliderect(g.fruit_hitboxes[k])) == 0

def test_multi_fruit():
    g = snake.game((10*side, 15*side))

    g.snake.head_x = 0
    g.snake.head_y = 0
    g.snake.head_hitbox.x = 0
    g.snake.head_hitbox.y = 1*side
    g.snake.body = [(0, 0)]
    g.snake.body_hitboxes = [pygame.Rect(0, 0, side, side)]

    x = 0
    for i in range(1, 9):
        y = i*side
        g.fruit_hitboxes.append(pygame.Rect(x, y, side, side))

    g.last_input = 's'

    for i in range(8):
        g.movement()

    assert g.snake.size == 10

    assert len(g.fruit_hitboxes) == 2

    g.fruit_hitboxes.clear()

    hy = g.snake.head_y // side

    for i in range(1, 5):
        y = (hy+i)*side
        g.fruit_hitboxes.append(pygame.Rect(x, y, side, side))

    for i in range(4):
        g.movement()

    assert g.snake.size == 14

    g.fruit_hitboxes.clear()

    hy = g.snake.head_y // side
    y = hy*side
    for i in range(1, 7):
        x = i*side
        g.fruit_hitboxes.append(pygame.Rect(x, y, side, side))

    g.last_input = 'd'

    for i in range(6):
        g.movement()

    assert g.snake.size == 20

    assert len(g.fruit_hitboxes) == 3

def test_game_over():
    g = snake.game((640, 640))

    g.snake.head_x = 1*side
    g.snake.head_y = 0

    g.snake.head_hitbox.x = side
    g.snake.head_hitbox.y = 0

    g.snake.body = [(0, 0), (side, 0)]

    g.snake.body_hitboxes = [pygame.Rect(0, 0, side, side), pygame.Rect(side, 0, side, side)]

    g.last_input = 'a'
    g.movement()

    assert g.game_over == True

    hx = g.snake.head_x
    hy = g.snake.head_y

    g.movement()

    assert g.snake.head_x == hx
    assert g.snake.head_y == hy


def test_opposing_keys():
    g = snake.game((640, 640))
    g.last_input = 's'
    g.movement()
    g.last_input = 'w'
    g.movement()
    assert g.prev_input == 's'

    g.last_input = 'd'
    g.movement()
    g.last_input = 'a'
    g.movement()
    assert g.prev_input == 'd'

    g.last_input = 'w'
    g.movement()
    g.last_input = 's'
    g.movement()
    assert g.prev_input == 'w'

    g.last_input = 'a'
    g.movement()
    g.last_input = 'd'
    g.movement()
    assert g.prev_input == 'a'

    