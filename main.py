import pygame
import time
import random

pygame.init()                                       # Iniciando o PyGame
screen = pygame.display.set_mode((400, 400))        # Iniciando a tela
font = pygame.font.Font(None, 36)                   # Definindo a fonte
sizes = [(10, 10), (15, 15), (20, 20)]              # Opcoes de tamanhos para o labirinto

buttons = []                                        # Criando os botoes
for i, size in enumerate(sizes):
    button = pygame.Rect(50, 50 + i * 50, 200, 40)
    buttons.append(button)

# Declarando as cores utilizadas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

running = True                                      # Configurando o loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Verifica se um botão foi clicado
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    maze_size = sizes[i]            # Determina o tamanho do labirinto
                    running = False

    screen.fill(WHITE)                              # Define o background como branco

    for i, button in enumerate(buttons):            # Desenhe os botões
        pygame.draw.rect(screen, BLACK, button, 2, border_radius=10)
        text = font.render(f"{sizes[i][0]} x {sizes[i][1]}", True, BLACK)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    instructions = font.render("Escolha um tamanho:", True, BLACK)  # Desenhe as instruções
    screen.blit(instructions, (50, 10))
    pygame.display.flip()                           # Atualiza a tela

pygame.quit()                                       # Fecha o pygame

FPS = 30
rows, cols = maze_size

pygame.init()               # inicializa o Pygame
pygame.mixer.init()
screen = pygame.display.set_mode((rows*20+40, cols*20+40))
screen.fill(WHITE)
pygame.display.set_caption("Gerador de Labirinto")
clock = pygame.time.Clock()

# Variaveis para o labirinto
x = 0
y = 0
w = 20 # largura da célula
grid = [[] for _ in range(rows)]
visited = []
stack = []
solution = {}

def build_grid(x, y, w):    # Constrói a grid
    for i in range(rows):
        x = 20
        y = y + 20
        for j in range(cols):
            pygame.draw.line(screen, BLACK, [x, y], [x + w, y])           # topo da célula
            pygame.draw.line(screen, BLACK, [x + w, y], [x + w, y + w])   # direita da célula
            pygame.draw.line(screen, BLACK, [x + w, y + w], [x, y + w])   # parte inferior da célula
            pygame.draw.line(screen, BLACK, [x, y + w], [x, y])           # à esquerda da célula
            grid.append((x,y))                                            # adiciona célula à lista de grid
            x = x + 20                                                    # move a célula para a nova posição

def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # desenha um retângulo com o dobro da largura da célula
    pygame.display.update()                                               # para mostrar a parede sendo removida

def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()

def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w +1, y +1, 39, 19), 0)
    pygame.display.update()

def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 39, 19), 0)
    pygame.display.update()

def single_cell( x, y):
    pygame.draw.rect(screen, YELLOW, (x +1, y +1, 18, 18), 0)       # desenha uma única célula
    pygame.display.update()

def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 18, 18), 0)        # usado para recolorir o caminho após single_cell
    pygame.display.update()                                        # celula visitada

def solution_cell(x,y):
    cell_width = 20
    radius = cell_width // 4
    pygame.draw.circle(screen, YELLOW, (x + cell_width // 2, y + cell_width // 2), radius) #Desenha um circulo amarelo
    pygame.display.update()                                        # celula visitada

def carve_out_maze(x, y):
    steps = 0
    single_cell(x, y)                                              # posição inicial do labirinto
    stack.append((x,y))                                            # coloca a célula inicial na pilha
    visited.append((x,y))                                          # adiciona célula inicial à lista visitada
    while len(stack) > 0:                                          # loop até que a pilha esteja vazia
        time.sleep(.07)
        cell = []                                                  # define a lista de células
        if (x + w, y) not in visited and (x + w, y) in grid:       # célula da direita disponível?
            cell.append("right")                                   # se sim adiciona à lista de células

        if (x - w, y) not in visited and (x - w, y) in grid:       # célula da esqueda disponível?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # célula de baixo disponível?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # célula de cima disponível?
            cell.append("up")

        if len(cell) > 0:                                          # verifica se a lista de células está vazia
            cell_chosen = (random.choice(cell))                    # seleciona uma das células aleatoriamente

            if cell_chosen == "right":                             # se esta célula foi escolhida
                push_right(x, y)                                   # chama a função push_right
                solution[(x + w, y)] = x, y                        # solução = chave do dicionário = nova célula, outra = célula atual
                x = x + w                                          # torna esta célula a célula atual
                visited.append((x, y))                             # adicionar à lista de visitados
                stack.append((x, y))                               # coloca a célula atual na pilha
                steps += 1
                print(f"{steps} passos.")

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))
                steps += 1
                print(f"{steps} passos.")

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))
                steps += 1
                print(f"{steps} passos.")

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
                steps += 1
                print(f"{steps} passos.")
        else:
            x, y = stack.pop()             # se não houver células disponíveis, retire uma da pilha
            single_cell(x, y)              # use a função single_cell para mostrar a imagem de retrocesso
            time.sleep(.05)
            backtracking_cell(x, y)        # mude a cor para verde para identificar o caminho de retorno
            steps += 1
            print(f"{steps} passos.")
    print(f"A busca cega encontrou a saída em {steps} passos.")

def plot_route_back(x, y):
    solution_cell(x, y)                   # lista de soluções contém todas as coordenadas para rotear de volta ao início
    steps = 0
    while (x, y) != (20,20):              # loop até a posição da célula == posição inicial
        x, y = solution[x, y]             # "key value" agora se torna a nova chave
        solution_cell(x, y)               # animação da rota de volta
        time.sleep(.1)
        steps += 1
    print(f"A busca informada e ncontrou a saída em {steps} passos.")

x, y = 20, 20                             # posição inicial da grade
build_grid(40, 0, 20)                     # 1º argumento = valor x, 2º argumento = valor y, 3º argumento = largura da célula
carve_out_maze(x,y)                       # chama a função de construção do labirinto
plot_route_back(rows*x, cols*y)           # chama a função de solução de plotagem

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     # verifica o fechamento da janela
            running = False