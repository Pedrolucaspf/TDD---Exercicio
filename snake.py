import os
import keyboard
import time

class Snake_body:
    head_x: int
    head_y: int
    body: list

    def __init__(self):
        self.head_x = 0
        self.head_y = 1
        self.body = [(0,0)]


class io_handler:
    
    x_size: int
    y_size: int
    game_speed: float
    last_input: str
    test_reconstruct: bool
    matrix = []
    snake: Snake_body

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
        
        self.game_speed = speed
        self.last_input = 's'
        self.snake = Snake_body()
        self.test_reconstruct = True
        self.matrix = []

        for i in range (self.y_size): 
            self.matrix.append([0]*self.x_size)

    def record_inputs(self):
        keyboard.add_hotkey('w', lambda: setattr(self, "last_input", 'w'))
        keyboard.add_hotkey('a', lambda: setattr(self, "last_input", 'a'))
        keyboard.add_hotkey('s', lambda: setattr(self, "last_input", 's'))
        keyboard.add_hotkey('d', lambda: setattr(self, "last_input", 'd'))
        keyboard.add_hotkey('esc', lambda: setattr(self, "last_input", 'end'))

    def display(self):
        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)
    
    def movement(self):
        
        if(self.test_reconstruct):
            self.snake.body = []
            for x in range(self.y_size):
                for y in range(self.x_size):
                    if(self.matrix[x][y] == 2):
                        self.snake.head_x = x
                        self.snake.head_y = y
                    elif(self.matrix[x][y] == 1):
                        self.snake.body.append((x, y))

        i = self.snake.head_x
        j = self.snake.head_y
        if(self.last_input == 'w'):
            new_x = (i-1)%self.y_size
            self.matrix[new_x][j] = 2
            self.matrix[i][j] = 1
            self.snake.head_x = new_x
            self.snake.body.insert(0, (i, j))
            k = self.snake.body[-1][0]
            l = self.snake.body[-1][1]
            self.matrix[k][l] = 0
            self.snake.body.pop()
        elif(self.last_input == 'a'):
            new_y = (j-1)%self.x_size
            self.matrix[i][new_y] = 2
            self.matrix[i][j] = 1
            self.snake.head_y = new_y
            self.snake.body.insert(0, (i, j))
            k = self.snake.body[-1][0]
            l = self.snake.body[-1][1]
            self.matrix[k][l] = 0
            self.snake.body.pop()
        elif(self.last_input == 's'):
            new_x = (i+1)%self.y_size
            self.matrix[new_x][j] = 2
            self.matrix[i][j] = 1
            self.snake.head_x = new_x
            self.snake.body.insert(0, (i, j))
            k = self.snake.body[-1][0]
            l = self.snake.body[-1][1]
            self.matrix[k][l] = 0
            self.snake.body.pop()
        elif(self.last_input == 'd'):
            new_y = (j+1)%self.x_size
            self.matrix[i][new_y] = 2
            self.matrix[i][j] = 1
            self.snake.head_y = new_y
            self.snake.body.insert(0, (i, j))
            k = self.snake.body[-1][0]
            l = self.snake.body[-1][1]
            self.matrix[k][l] = 0
            self.snake.body.pop()
            

### exemplo do uso da classe io_handler  
instance = io_handler((10,15), 0.5)
instance.matrix[0][0] = 1 #corpo
instance.matrix[0][1] = 2 #cabeça
instance.matrix[0][2] = 3 #fruta

def game_loop():
    instance.test_reconstruct = False
    instance.record_inputs()
    while True:
        instance.movement()
        instance.display()
        print("mova com WASD, saia com esc. Ultimo botão:", end=' ')
        ###adicione seu código para lidar com o jogo aqui
        
        print(instance.last_input)
        if(instance.last_input == 'end'):
            exit()
        time.sleep(instance.game_speed)

if __name__ == "__main__":
    game_loop()