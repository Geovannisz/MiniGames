import pygame, sys, random, time

# Definir tamanho da tela
screen_width = 720
screen_height = 480

# Definir cores
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Criar a tela
screen = pygame.display.set_mode((screen_width, screen_height))

# Definir título da janela
pygame.display.set_caption('Jogo da Cobrinha')

# Definir ícone da janela
icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(icon)

# Definir FPS (frames per second)
fps = pygame.time.Clock()

# Definir tamanho dos segmentos da cobra
snake_size = 20

# Definir velocidade da cobra
snake_speed = 15

# Criar a cobra
snake = []
for i in range(5):
    x = 250 - i*snake_size
    y = 250
    snake.append((x, y))

# Definir direção inicial da cobra
direction = 'right'

# Gerar posição inicial da comida
food_pos = [random.randrange(1, (screen_width//snake_size)) * snake_size,
            random.randrange(1, (screen_height//snake_size)) * snake_size]
food_spawn = True

# Criar a comida
food = pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size)

# Função para desenhar a cobra
def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

# Função para mover a cobra
def move_snake():
    global snake
    # Remover o último segmento da cobra
    snake.pop()
    # Adicionar novo segmento à cobra
    if direction == 'right':
        new_head = (snake[0][0] + snake_size, snake[0][1])
    elif direction == 'left':
        new_head = (snake[0][0] - snake_size, snake[0][1])
    elif direction == 'up':
        new_head = (snake[0][0], snake[0][1] - snake_size)
    elif direction == 'down':
        new_head = (snake[0][0], snake[0][1] + snake_size)
    snake = [new_head] + snake

# Função para verificar se o jogo acabou
def check_game_over():
    global snake
    # Verificar se a cobra saiu da tela
    if snake[0][0] < 0 or snake[0][0] >= screen_width or snake[0][1] < 0 or snake[0][1] >= screen_height:
        return True
    # Verificar se a cobra se colidiu consigo mesma
    for i in range(1, len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True
    return False

# Função principal do jogo
def main():
    global direction, snake, food, food_spawn

    while True:
        # Verificar se o jogador perdeu o jogo
        if check_game_over():
            print('Você perdeu!')
            pygame.quit()
            sys.exit()

        # Verificar eventos do jogador
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'

        # Atualizar posição da cobra
        move_snake()

        # Verificar se a cobra comeu a comida
        if snake[0][0] == food.x and snake[0][1] == food.y:
            food_spawn = False
        else:
            # Remover o último segmento da cobra
            snake.pop()

        # Gerar nova comida se necessário
        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width//snake_size)) * snake_size,
                        random.randrange(1, (screen_height//snake_size)) * snake_size]
            food = pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size)
            food_spawn = True

        # Preencher tela com cor de fundo
        screen.fill(black)

        # Desenhar cobra e comida
        draw_snake(snake)
        pygame.draw.rect(screen, white, food)

        # Atualizar tela
        pygame.display.update()

        # Definir FPS
        fps.tick(snake_speed)

# Executar o jogo
main()

