#from snake import io_handler
from snake_ref import io_handler
import pytest

@pytest.fixture
def handler():
    instance = io_handler((10, 15), 0.5)
    instance.matrix[0][0] = 1 #corpo
    instance.matrix[0][1] = 2 #cabeça
    instance.matrix[0][2] = 3 #fruta
    return instance

def test_handler_mov_d(handler):
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