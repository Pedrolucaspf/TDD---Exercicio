import pygame
import random

pygame.init()

w = 640
h = 640

screen = pygame.display.set_mode((w, h))

head_u_img = pygame.image.load('Graphics/head_up.png').convert()
head_d_img = pygame.image.load('Graphics/head_down.png').convert()
head_l_img = pygame.image.load('Graphics/head_left.png').convert()
head_r_img = pygame.image.load('Graphics/head_right.png').convert()

tail_u_img = pygame.image.load('Graphics/tail_up.png').convert()
tail_d_img = pygame.image.load('Graphics/tail_down.png').convert()
tail_l_img = pygame.image.load('Graphics/tail_left.png').convert()
tail_r_img = pygame.image.load('Graphics/tail_right.png').convert()

body_v_img = pygame.image.load('Graphics/body_vertical.png').convert()
body_h_img = pygame.image.load('Graphics/body_horizontal.png').convert()
body_tl_img = pygame.image.load('Graphics/body_topleft.png').convert()
body_tr_img = pygame.image.load('Graphics/body_topright.png').convert()
body_bl_img = pygame.image.load('Graphics/body_bottomleft.png').convert()
body_br_img = pygame.image.load('Graphics/body_bottomright.png').convert()

fruit_img = pygame.image.load('Graphics/apple.png').convert()

side_len = head_u_img.get_width()

class Snake_body:
    head_x: int
    head_y: int
    size: int
    body: list
    seg_dir: list
    head_hitbox: pygame.rect
    body_hitboxes: list

    def __init__(self):
        self.head_x = 0
        self.head_y = 1 * side_len  
        self.head_hitbox = pygame.Rect(self.head_x, self.head_y, side_len, side_len)
        self.size = 2
        self.body = [(0,0)]
        self.seg_dir = ['h']
        self.body_hitboxes = []
        self.body_hitboxes.insert(0, pygame.Rect(self.body[0][0], self.body[0][1], side_len, side_len))

class game:
    
    x_size: int
    y_size: int
    fruit_hitboxes: list
    last_input: str
    prev_input: str
    running: bool
    game_over: bool
    snake: Snake_body

    def __init__(self, dim):
        self.x_size = dim[0]
        self.y_size = dim[1]
        self.fruit_hitboxes = []
        self.last_input = 'd'
        self.prev_input = 'd'
        self.snake = Snake_body()
        self.game_over = False
        self.running = True

    def display(self, screen):
        if(self.last_input == 'w'):
            screen.blit(head_u_img, (self.snake.head_x, self.snake.head_y))
        elif(self.last_input == 'a'):
            screen.blit(head_l_img, (self.snake.head_x, self.snake.head_y))
        elif(self.last_input == 's'):
            screen.blit(head_d_img, (self.snake.head_x, self.snake.head_y))
        elif(self.last_input == 'd'):
            screen.blit(head_r_img, (self.snake.head_x, self.snake.head_y))
        
        for k in range(self.snake.size-1):
            screen.blit(body_h_img, (self.snake.body_hitboxes[k].x, self.snake.body_hitboxes[k].y))

        for k in range(len(self.fruit_hitboxes)):
            screen.blit(fruit_img, (self.fruit_hitboxes[k].x, self.fruit_hitboxes[k].y))

    def movement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.last_input = 'w'
                elif event.key == pygame.K_a:
                    self.last_input = 'a'
                elif event.key == pygame.K_s:
                    self.last_input = 's'
                elif event.key == pygame.K_d:
                    self.last_input = 'd'
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    return

        if(self.game_over == False):

            if(self.prev_input == 's' and self.last_input == 'w'):
               self.last_input = 's'
            elif(self.prev_input == 'w' and self.last_input == 's'):
               self.last_input = 'w'
            elif(self.prev_input == 'a' and self.last_input == 'd'):
               self.last_input = 'a'
            elif(self.prev_input == 'd' and self.last_input == 'a'):
               self.last_input = 'd'
            else:
                self.prev_input = self.last_input       

            i = self.snake.head_x
            j = self.snake.head_y
            erase_last = True

            new_x = i
            new_y = j
            if(self.last_input == 'w'):
                new_y = (j - side_len)%self.y_size

            elif(self.last_input == 'a'):
                new_x = (i - side_len)%self.x_size

            elif(self.last_input == 's'):
                new_y = (j + side_len)%self.y_size

            elif(self.last_input == 'd'):
                new_x = (i + side_len)%self.x_size

            new_head_hitbox = pygame.Rect(new_x, new_y, side_len, side_len)
            
            for k in range(len(self.snake.body_hitboxes)):
                if(new_head_hitbox.colliderect(self.snake.body_hitboxes[k])):
                    if(erase_last == True and k == len(self.snake.body_hitboxes)-1):
                        continue

                    self.game_over = True
                    return
                
            for k in range(len(self.fruit_hitboxes) - 1, -1, -1):
                if(new_head_hitbox.colliderect(self.fruit_hitboxes[k])):
                    self.snake.size += 1
                    self.fruit_hitboxes.pop(k)
                    erase_last = False            

            self.snake.head_x = new_x
            self.snake.head_y = new_y
            self.snake.head_hitbox = new_head_hitbox

            if(self.last_input != 'end'):
                self.snake.body.insert(0, (i, j))
                self.snake.body_hitboxes.insert(0, pygame.Rect(self.snake.body[0][0], self.snake.body[0][1], body_h_img.get_width(), body_h_img.get_height()))
                if(erase_last == True):
                    self.snake.body.pop()
                    self.snake.body_hitboxes.pop()
                elif(len(self.fruit_hitboxes) == 0):
                        self.spawn_fruit()
            
    def spawn_fruit(self):
        num_fruits = 1 + (self.snake.size//10) # Arredonda para baixo
        for i in range(num_fruits):
            fruit_spawned = 0
            fruit = pygame.Rect(-1000, -1000, fruit_img.get_width(), fruit_img.get_height())
            while(fruit_spawned == 0):
                x = random.randint(2*side_len, self.y_size) - side_len
                y = random.randint(2*side_len, self.x_size) - side_len
                fruit.x = x
                fruit.y = y
                collided = 0
                if(fruit.colliderect(self.snake.head_hitbox)):
                    collided = 1
                
                for i in range(self.snake.size-1):
                    if(fruit.colliderect(self.snake.body_hitboxes[i])):
                        collided = 1
                        break
                    
                if(collided == 0):
                    fruit_spawned = 1
                    self.fruit_hitboxes.append(fruit)

def game_loop():
    instance = game((w, h))
    instance.spawn_fruit()

    myfont = pygame.font.SysFont("monospace", 40)

    clock = pygame.time.Clock()
    
    move_timer = 0
    move_delay = 0.15  # segundos entre movimentos
    delta_time = 0.1

    while instance.running:
        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))
        move_timer += delta_time

        if move_timer >= move_delay:
            instance.movement() 
            move_timer = 0

        screen.fill((255, 255, 255))
        instance.display(screen)

        if(instance.game_over == True):
            label = myfont.render(f"Pontuação final: {instance.snake.size}", 1, (0,255,0))
            screen.blit(label, (w/6, h/3))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()

