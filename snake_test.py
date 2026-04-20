from snake import io_handler
#from snake_ref import io_handler
import pytest

@pytest.fixture
def handler():
    instance = io_handler((10, 15), 0.5)
    instance.matrix[0][0] = 1 #corpo
    instance.matrix[0][1] = 2 #cabeça
    instance.matrix[0][5] = 3 #fruta
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
    
     