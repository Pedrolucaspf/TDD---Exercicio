#from snake import io_handler
from snake_ref import io_handler
import pytest

@pytest.fixture
def handler():
    instance = io_handler((10, 15), 0.5)
    instance.matrix[0][0] = 1 #corpo
    instance.matrix[0][1] = 2 #cabeça
    instance.matrix[0][5] = 3 #fruta
    return instance

@pytest.fixture
def handler_multi():
    instance = io_handler((10, 15), 0.5)
    instance.matrix[0][0] = 1 
    instance.matrix[0][1] = 2
    for i in range(1, 9): 
        instance.matrix[i][1] = 3
        instance.fruit_count += 1

    instance.last_input = 's'
    for i in range(8):
        instance.movement()

    return instance

def test_handler_mov(handler):
    handler.last_input = 'd'
    handler.movement()
    assert handler.matrix[0][2] == 2
    assert handler.matrix[0][1] == 1

    handler.movement()
    assert handler.matrix[0][3] == 2
    assert handler.matrix[0][2] == 1

    handler.last_input = 's'
    handler.movement()
    assert handler.matrix[1][3] == 2
    assert handler.matrix[0][3] == 1

    handler.movement()
    assert handler.matrix[2][3] == 2
    assert handler.matrix[1][3] == 1

    handler.last_input = 'a'
    handler.movement()
    assert handler.matrix[2][2] == 2
    assert handler.matrix[2][3] == 1

    handler.last_input = 'w'
    handler.movement()
    assert handler.matrix[1][2] == 2
    assert handler.matrix[2][2] == 1

@pytest.mark.parametrize("x_before, change_x, y_before, change_y, key", [
    (0, 0, -1, 1, 'd'),
    (-1, 0, 0, -1, 'a'),
    (-1, 1, 0, 0, 's'),
    (0, -1, -1, 0, 'w'),
])

def test_boundaries(x_before, change_x, y_before, change_y, key):
    instance = io_handler((10, 15), 0.5)
    instance.matrix[x_before][y_before] = 2
    instance.last_input = key
    instance.snake.head_x = x_before
    instance.snake.head_y = y_before

    x_after = (x_before + change_x) % instance.y_size
    y_after = (y_before + change_y) % instance.x_size

    if(x_before == x_after):
        instance.matrix[x_before][y_before-change_y] = 1
        instance.movement()
        assert instance.matrix[x_before][y_after] == 2
        assert instance.matrix[x_before][y_before] == 1

        for i in range(instance.x_size):
            instance.movement()

        assert instance.matrix[x_before][y_after] == 2
        assert instance.matrix[x_before][y_after-change_y] == 1

    elif(y_before == y_after):
        instance.matrix[x_before-change_x][y_before] = 1
        instance.movement()
        assert instance.matrix[x_after][y_before] == 2
        assert instance.matrix[x_before][y_before] == 1

        for i in range(instance.y_size):
            instance.movement()
        
        assert instance.matrix[x_after][y_before] == 2
        assert instance.matrix[x_after-change_x][y_before] == 1

def test_disappear(handler):
    handler.last_input = 's'
    for i in range(3):
        handler.movement()
    
    assert handler.matrix[0][0] == 0
    assert handler.matrix[0][1] == 0
    assert handler.matrix[1][1] == 0

    
def test_eat_fruit(handler):
    handler.last_input = 'd'
    handler.test_reconstruct = False
    for i in range(4):
        handler.movement()
        
    assert handler.snake.size == 3
    assert handler.matrix[0][5] == 2
    assert handler.matrix[0][4] == 1
    assert handler.matrix[0][3] == 1
    
    fruit_present = False

    for x in range(handler.y_size):
        for y in range(handler.x_size):
            if(handler.matrix[x][y] == 3):
                fruit_present = True
            
        
    assert fruit_present == True


def test_multi_fruit(handler_multi):
    assert handler_multi.snake.size == 10
    assert handler_multi.fruit_count == 2
    
    for x in range(handler_multi.y_size):
                for y in range(handler_multi.x_size):
                    if(handler_multi.matrix[x][y] == 3):
                        handler_multi.matrix[x][y] = 0
                        handler_multi.fruit_count -= 1

    hx = handler_multi.snake.head_x
    hy = handler_multi.snake.head_y
    for i in range(1, 5): 
        handler_multi.matrix[hx+i][hy] = 3
        handler_multi.fruit_count += 1

    hx += 4

    for i in range(4):
        handler_multi.movement()
    
    assert handler_multi.snake.size == 14

    for x in range(handler_multi.y_size):
        for y in range(handler_multi.x_size):
            if(handler_multi.matrix[x][y] == 3):
                handler_multi.matrix[x][y] = 0
                handler_multi.fruit_count -= 1

    for i in range(1, 7): 
        handler_multi.matrix[hx][hy+i] = 3
        handler_multi.fruit_count += 1

    handler_multi.last_input = 'd'
    for i in range(6):
        handler_multi.movement()

    assert handler_multi.snake.size == 20
    assert handler_multi.fruit_count == 3


def test_game_over(handler_multi):
    handler_multi.last_input = 'd'
    for i in range(2):
        handler_multi.movement()
    
    handler_multi.last_input = 'w'
    handler_multi.movement()
    
    handler_multi.last_input = 'a'
    handler_multi.movement()

    hx = handler_multi.snake.head_x
    hy = handler_multi.snake.head_y

    handler_multi.movement()

    assert handler_multi.game_over == True

    handler_multi.movement()

    assert handler_multi.snake.head_x == hx
    assert handler_multi.snake.head_y == hy