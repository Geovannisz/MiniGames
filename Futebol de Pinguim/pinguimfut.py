import pygame
import math
import time

# Inicialização do Pygame
pygame.init()


# Constantes do jogo
TELA_LARGURA, TELA_ALTURA = 1200, 800  # Tamanho do campo aumentado
COR_BG = (80, 200, 80)  # Cor de fundo (azul)
VELOCIDADE_PINGUIM = 5
VELOCIDADE_BOLA = 12
VELOCIDADE_BOT = 3
COR_PINGUIM = (0, 0, 0)  # Cor do pinguim (preto)
COR_BICO_PES = (255, 165, 0)  # Cor do bico e dos pés (laranja)
COR_BOLA = (255, 255, 255)  # Cor da bola (branco)
TAMANHO_GOL = (50, 150)  # Tamanho do gol alterado para ser maior verticalmente
COR_TEXTO = (255, 255, 255)  # Cor do texto (branco)
FONT = pygame.font.Font(None, 36)
TEMPO_JOGO = 60  # Tempo de duração do jogo em segundos


# Constantes do jogo
TELA_LARGURA, TELA_ALTURA = 1200, 800  # Tamanho do campo aumentado
COR_BG = (80, 200, 80)  # Cor de fundo (azul)
VELOCIDADE_PINGUIM = 5
VELOCIDADE_BOLA = 12
VELOCIDADE_BOT = 3
COR_PINGUIM = (0, 0, 0)  # Cor do pinguim (preto)
COR_BICO_PES = (255, 165, 0)  # Cor do bico e dos pés (laranja)
COR_BOLA = (255, 255, 255)  # Cor da bola (branco)
TAMANHO_GOL = (50, 150)  # Tamanho do gol alterado para ser maior verticalmente
COR_TEXTO = (255, 255, 255)  # Cor do texto (branco)
FONT = pygame.font.Font(None, 36)
TEMPO_JOGO = 60  # Tempo de duração do jogo em segundos
rodando = True

# Função para mostrar o menu inicial
def mostrar_menu(tela):
    menu_font = pygame.font.Font(None, 74)
    mensagem = menu_font.render('Penguinfut 2023', True, COR_TEXTO)
    mensagem_rect = mensagem.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 - 50))

    iniciar_jogo_font = pygame.font.Font(None, 50)
    iniciar_mensagem = iniciar_jogo_font.render('Pressione Enter para iniciar', True, COR_TEXTO)
    iniciar_mensagem_rect = iniciar_mensagem.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 50))

    tela.fill(COR_BG)
    tela.blit(mensagem, mensagem_rect)
    tela.blit(iniciar_mensagem, iniciar_mensagem_rect)
    pygame.display.flip()

    menu_aberto = True
    while menu_aberto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    menu_aberto = False

# Inicializar a tela
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("Futebol de Pinguim")
def bola_no_gol(bola_rect, gol_rect):
    return gol_rect.colliderect(bola_rect)
# Mostrar menu inicial antes de iniciar o jogo
mostrar_menu(tela)


# Configurações de tela
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("Futebol de Pinguins")

# Classe para o jogador pinguim
class Pinguim(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, cor):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        # Corpo do pinguim
        pygame.draw.ellipse(self.image, cor, [0, 0, 50, 70])
        # Barriga branca
        pygame.draw.ellipse(self.image, (255, 255, 255), [10, 20, 30, 45])
        # Bico do pinguim
        pygame.draw.polygon(self.image, COR_BICO_PES, [(25, 15), (20, 5), (30, 5)])
        # Olhos do pinguim
        pygame.draw.ellipse(self.image, (255, 255, 255), [15, 0, 10, 10])
        pygame.draw.ellipse(self.image, (255, 255, 255), [25, 0, 10, 10])
        pygame.draw.ellipse(self.image, (0, 0, 0), [17, 3, 6, 6])
        pygame.draw.ellipse(self.image, (0, 0, 0), [27, 3, 6, 6])
        # Pés do pinguim
        pygame.draw.ellipse(self.image, COR_BICO_PES, [15, 65, 10, 5])
        pygame.draw.ellipse(self.image, COR_BICO_PES, [25, 65, 10, 5])
        
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidade = VELOCIDADE_PINGUIM

    def mover(self, direcao):
        if direcao == 'ESQUERDA' and self.rect.left > 0:
            self.rect.x -= self.velocidade
        elif direcao == 'DIREITA' and self.rect.right < TELA_LARGURA:
            self.rect.x += self.velocidade
        elif direcao == 'CIMA' and self.rect.top > 0:
            self.rect.y -= self.velocidade
        elif direcao == 'BAIXO' and self.rect.bottom < TELA_ALTURA:
            self.rect.y += self.velocidade

# Classe para o bot adversário
class Bot(Pinguim):
    def __init__(self, pos_x, pos_y, cor):
        super().__init__(pos_x, pos_y, cor)
        self.dash_velocidade = 10  # Diminuir a velocidade do dash
        self.dash_tempo = 0.5  # Duração do dash em segundos
        self.inicio_dash = None  # Para controlar o início do dash
        self.velocidade = pygame.math.Vector2(0, 0)  # Adicionado para controlar a velocidade do dash

    def mover_para_bola(self, bola):
        # Se estiver em dash, não mover em direção à bola
        if self.inicio_dash is not None and time.time() - self.inicio_dash < self.dash_tempo:
            return
        delta_x = bola.rect.centerx - self.rect.centerx
        delta_y = bola.rect.centery - self.rect.centery
        distancia = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if distancia > 0:
            direcao = pygame.math.Vector2(delta_x / distancia, delta_y / distancia)
            self.rect.x += direcao.x * VELOCIDADE_BOT
            self.rect.y += direcao.y * VELOCIDADE_BOT
        # Restringir movimento do bot dentro do campo
        self.rect.clamp_ip(pygame.Rect(0, 0, TELA_LARGURA, TELA_ALTURA))

    def update(self):
        # Atualizar posição durante o dash
        if self.inicio_dash and time.time() - self.inicio_dash >= self.dash_tempo:
            self.velocidade = pygame.math.Vector2(0, 0)
            self.inicio_dash = None
        self.rect.x += self.velocidade.x
        self.rect.y += self.velocidade.y
        self.rect.clamp_ip(pygame.Rect(0, 0, TELA_LARGURA, TELA_ALTURA))

    def dash(self, direcao):
        self.velocidade = direcao * self.dash_velocidade
        self.inicio_dash = time.time()

# Classe para a bola com atrito
class Bola(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)  # Tamanho aumentado
        pygame.draw.ellipse(self.image, COR_BOLA, [0, 0, 40, 40])  # Desenho da bola aumentado
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.velocidade = pygame.math.Vector2(0, 0)
        self.atrito = 0.06  # Valor pequeno para simular o atrito

    def update(self):
        self.rect.x += self.velocidade.x
        self.rect.y += self.velocidade.y

        # Aplicar atrito para reduzir a velocidade da bola gradualmente
        if self.velocidade.length() > 0:  # Verifica se a velocidade não é zero
            self.velocidade -= self.velocidade.normalize() * self.atrito

            # Se a velocidade for muito baixa, pare a bola
            if self.velocidade.length() < self.atrito:
                self.velocidade = pygame.math.Vector2(0, 0)

        # Mantém a bola dentro da tela e adiciona uma força extra nas bordas e cantos
        if self.rect.left < 0:
            self.velocidade.x = abs(self.velocidade.x)
            self.velocidade += pygame.math.Vector2(1, 0)  # Força extra para direita
        if self.rect.right > TELA_LARGURA:
            self.velocidade.x = -abs(self.velocidade.x)
            self.velocidade -= pygame.math.Vector2(1, 0)  # Força extra para esquerda
        if self.rect.top < 0:
            self.velocidade.y = abs(self.velocidade.y)
            self.velocidade += pygame.math.Vector2(0, 1)  # Força extra para baixo
        if self.rect.bottom > TELA_ALTURA:
            self.velocidade.y = -abs(self.velocidade.y)
            self.velocidade -= pygame.math.Vector2(0, 1)  # Força extra para cima

        # Adiciona uma força extra nos cantos para afastar a bola mais eficientemente
        if self.rect.left < 10 and self.rect.top < 10:
            self.velocidade += pygame.math.Vector2(1, 1)  # Força extra para baixo-direita
        if self.rect.right > TELA_LARGURA - 10 and self.rect.top < 10:
            self.velocidade += pygame.math.Vector2(-1, 1)  # Força extra para baixo-esquerda
        if self.rect.left < 10 and self.rect.bottom > TELA_ALTURA - 10:
            self.velocidade += pygame.math.Vector2(1, -1)  # Força extra para cima-direita
        if self.rect.right > TELA_LARGURA - 10 and self.rect.bottom > TELA_ALTURA - 10:
            self.velocidade += pygame.math.Vector2(-1, -1)  # Força extra para cima-esquerda
        

    def chutar(self, pinguim):
        # Calcula o vetor normalizado da direção do chute
        delta_x = self.rect.centerx - pinguim.rect.centerx
        delta_y = self.rect.centery - pinguim.rect.centery
        distancia = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if distancia == 0:  # Evita divisão por zero
            return
        direcao = pygame.math.Vector2(delta_x / distancia, delta_y / distancia)
        # Aplica a velocidade de chute na direção calculada
        self.velocidade = direcao * VELOCIDADE_BOLA



# Função para reiniciar o jogo
def reiniciar_jogo():
    global placar_jogador, placar_bot, inicio_jogo
    jogador.rect.center = (TELA_LARGURA // 4, TELA_ALTURA // 2)
    bot.rect.center = (3 * TELA_LARGURA // 4, TELA_ALTURA // 2)
    bola.rect.center = (TELA_LARGURA // 2, TELA_ALTURA // 2)
    bola.velocidade = pygame.math.Vector2(0, 0)
    placar_jogador, placar_bot = 0, 0
    inicio_jogo = time.time()

# Função para checar e resolver colisões entre pinguins
def checar_colisao_pinguins(pinguim1, pinguim2):
    if pygame.sprite.collide_rect(pinguim1, pinguim2):
        dx = pinguim1.rect.centerx - pinguim2.rect.centerx
        dy = pinguim1.rect.centery - pinguim2.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:  # Evita divisão por zero
            return
        dx, dy = dx / dist, dy / dist  # Normalização do vetor
        pinguim1.rect.x += int(dx * pinguim1.velocidade)
        pinguim1.rect.y += int(dy * pinguim1.velocidade)
        
        # Corrigir a multiplicação pelo valor de velocidade, que deve ser um inteiro
        if isinstance(pinguim2.velocidade, pygame.math.Vector2):
            pinguim2.rect.x -= int(dx * pinguim2.velocidade.length())
            pinguim2.rect.y -= int(dy * pinguim2.velocidade.length())
        else:
            pinguim2.rect.x -= int(dx * pinguim2.velocidade)
            pinguim2.rect.y -= int(dy * pinguim2.velocidade)

# Função para chutar outro pinguim com proximidade
def chutar_bot(pinguim, bot, forca_dash):
    # Calcula a distância entre o pinguim e o bot
    dx = bot.rect.centerx - pinguim.rect.centerx
    dy = bot.rect.centery - pinguim.rect.centery
    dist = math.hypot(dx, dy)
    
    # Verifica se o pinguim está suficientemente próximo para chutar o bot
    if dist < 80:  # Aumentar o alcance do chute
        direcao = pygame.math.Vector2(dx, dy).normalize()
        bot.dash(direcao)


# Grupo de sprites
todos_sprites = pygame.sprite.Group()

# Placar
placar_jogador = 0
placar_bot = 0

# Criar um jogador, um bot e uma bola
jogador = Pinguim(TELA_LARGURA // 4, TELA_ALTURA // 2, COR_PINGUIM)
bot = Bot(3 * TELA_LARGURA // 4, TELA_ALTURA // 2, (255, 0, 0))  # Bot é vermelho
bola = Bola(TELA_LARGURA // 2, TELA_ALTURA // 2 + 100)
todos_sprites.add(jogador)
todos_sprites.add(bot)
todos_sprites.add(bola)

# Definindo os gols
gol_esquerda_rect = pygame.Rect(0, (TELA_ALTURA - TAMANHO_GOL[1]) // 2, TAMANHO_GOL[0], TAMANHO_GOL[1])
gol_direita_rect = pygame.Rect(TELA_LARGURA - TAMANHO_GOL[0], (TELA_ALTURA - TAMANHO_GOL[1]) // 2, TAMANHO_GOL[0], TAMANHO_GOL[1])

# Iniciar o tempo do jogo
inicio_jogo = time.time()

# Loop principal do jogo

clock = pygame.time.Clock()
mostrar_vencedor = False

while rodando:
    tempo_atual = time.time()
    tempo_restante = TEMPO_JOGO - (tempo_atual - inicio_jogo)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    if not mostrar_vencedor:
        # Atualizar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jogador.mover('ESQUERDA')
        if keys[pygame.K_RIGHT]:
            jogador.mover('DIREITA')
        if keys[pygame.K_UP]:
            jogador.mover('CIMA')
        if keys[pygame.K_DOWN]:
            jogador.mover('BAIXO')

        # Mover o bot em direção à bola
        bot.mover_para_bola(bola)

        # No loop principal do jogo, após mover o bot em direção à bola:
        bot.update()

        # Atualizar a bola
        bola.update()

        # Verificar colisões para chutar a bola
        if jogador.rect.colliderect(bola.rect):
            bola.chutar(jogador)
        if bot.rect.colliderect(bola.rect):
            bola.chutar(bot)

        # Verificar se a bola entrou em algum gol
        elif bola_no_gol(bola.rect, gol_esquerda_rect):
            placar_bot += 1
            bola.rect.center = (TELA_LARGURA // 2, TELA_ALTURA // 2)
            jogador.rect.center = (TELA_LARGURA // 4, TELA_ALTURA // 2)
            bot.rect.center = (3 * TELA_LARGURA // 4, TELA_ALTURA // 2)
            bola.velocidade = pygame.math.Vector2(0, 0)
        elif bola_no_gol(bola.rect, gol_direita_rect):
            placar_jogador += 1
            bola.rect.center = (TELA_LARGURA // 2, TELA_ALTURA // 2)
            jogador.rect.center = (TELA_LARGURA // 4, TELA_ALTURA // 2)
            bot.rect.center = (3 * TELA_LARGURA // 4, TELA_ALTURA // 2)
            bola.velocidade = pygame.math.Vector2(0, 0)
        # Verificar o tempo de jogo
        if tempo_restante <= 0:
            mostrar_vencedor = True
            inicio_mostrar_vencedor = tempo_atual

        # Verificar colisões entre pinguins
        checar_colisao_pinguins(jogador, bot)
        
        # No loop principal do jogo:
        if keys[pygame.K_SPACE]:
            chutar_bot(jogador, bot, bot.dash_velocidade)

        # Atualizar a bola aplicando o atrito
        bola.update()
        

    # Desenhar
    tela.fill(COR_BG)
    pygame.draw.rect(tela, COR_TEXTO, gol_esquerda_rect, 2)  # Desenhar o gol esquerdo
    pygame.draw.rect(tela, COR_TEXTO, gol_direita_rect, 2)  # Desenhar o gol direito
    todos_sprites.draw(tela)

    # Desenhar o placar
    if not mostrar_vencedor:
        placar_texto = FONT.render(f'Jogador: {placar_jogador} Bot: {placar_bot}', True, COR_TEXTO)
        tela.blit(placar_texto, (TELA_LARGURA // 2 - placar_texto.get_width() // 2, 10))
        tempo_texto = FONT.render(f'Tempo: {int(tempo_restante)}', True, COR_TEXTO)
        tela.blit(tempo_texto, (10, 10))
    else:
        # Identificar o vencedor
        vencedor = "Jogador" if placar_jogador > placar_bot else "Bot" if placar_bot > placar_jogador else "Empate"
        vencedor_texto = FONT.render(f'Vencedor: {vencedor}', True, COR_TEXTO)
        tela.blit(vencedor_texto, (TELA_LARGURA // 2 - vencedor_texto.get_width() // 2, TELA_ALTURA // 2 - 20))
        placar_texto = FONT.render(f'Placar final: Jogador {placar_jogador} - {placar_bot} Bot', True, COR_TEXTO)
        tela.blit(placar_texto, (TELA_LARGURA // 2 - placar_texto.get_width() // 2, TELA_ALTURA // 2 + 20))

        # Verificar se devemos reiniciar o jogo
        if tempo_atual - inicio_mostrar_vencedor > 5:
            mostrar_vencedor = False
            reiniciar_jogo()

    pygame.display.flip()

    # Manter o jogo rodando a 60fps
    clock.tick(60)

# Finalizar Pygame
pygame.quit()