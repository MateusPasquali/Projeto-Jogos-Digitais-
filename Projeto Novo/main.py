import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pandemia: Invasão Zombie")

# Plano de fundo
fundo = pygame.image.load('fundo.jpg')
fundo = pygame.transform.scale(fundo, (largura, altura))

# Cores
BRANCO = (255, 255, 255)

# Personagem
personagem_imagem = pygame.image.load('personagem.png')
personagem_rect = personagem_imagem.get_rect()
personagem_rect.center = (largura // 2, altura // 2)
personagem_speed = 5

# Inimigos
inimigos = []
inimigo_imagem = pygame.image.load('inimigo.png')
inimigo_speed = 1

# Balas
balas = []
bala_imagem = pygame.image.load('bala.png')
balas_disponiveis = 12

# Pontuação
pontuacao = 0

# Vida do personagem
vida_personagem = 150

# Fonte
fonte = pygame.font.Font(None, 36)

# Número da rodada
round_atual = 0
max_inimigos_round = 1

def iniciar_round():
    global round_atual, inimigos, max_inimigos_round
    round_atual += 1
    inimigos = []
    for _ in range(max_inimigos_round):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        inimigos.append([x, y])
    max_inimigos_round += 1  # Aumenta o número de inimigos a cada rodada

iniciar_round()

# Configuração do clock
clock = pygame.time.Clock()
FPS = 30  # Defina a taxa de quadros por segundo desejada

# Loop principal do jogo
jogando = True
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    # Atualização do clock
    clock.tick(FPS)

    # Movimentação do personagem
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        personagem_rect.y -= personagem_speed
    if teclas[pygame.K_s]:
        personagem_rect.y += personagem_speed
    if teclas[pygame.K_a]:
        personagem_rect.x -= personagem_speed
    if teclas[pygame.K_d]:
        personagem_rect.x += personagem_speed

    # Atualização da direção do personagem em relação ao mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    direcao_x = mouse_x - personagem_rect.centerx
    direcao_y = mouse_y - personagem_rect.centery
    angulo = math.atan2(direcao_y, direcao_x)
    personagem_rotacionado = pygame.transform.rotate(personagem_imagem, math.degrees(angulo))
    personagem_rect = personagem_rotacionado.get_rect(center=personagem_rect.center)

    # Atualização da posição dos inimigos em relação ao jogador
    for inimigo in inimigos:
        direcao_x = personagem_rect.centerx - inimigo[0]
        direcao_y = personagem_rect.centery - inimigo[1]
        angulo = math.atan2(direcao_y, direcao_x)
        inimigo[0] += math.cos(angulo) * inimigo_speed
        inimigo[1] += math.sin(angulo) * inimigo_speed

    # Disparo de balas
    if pygame.mouse.get_pressed()[0] and balas_disponiveis > 0:
        bala_x = personagem_rect.centerx
        bala_y = personagem_rect.centery
        direcao_x = mouse_x - bala_x
        direcao_y = mouse_y - bala_y
        angulo = math.atan2(direcao_y, direcao_x)
        bala_vel_x = math.cos(angulo) * 10
        bala_vel_y = math.sin(angulo) * 10
        balas.append([bala_x, bala_y, bala_vel_x, bala_vel_y])
        balas_disponiveis -= 1

    # Atualização das balas
    balas = [[x + vel_x, y + vel_y, vel_x, vel_y] for x, y, vel_x, vel_y in balas]

    # Remoção das balas que saíram da tela
    balas = [bala for bala in balas if 0 < bala[0] < largura and 0 < bala[1] < altura]

    # Detecção de colisão entre balas e inimigos
    for inimigo in inimigos:
        colisoes = [bala for bala in balas if pygame.Rect(inimigo[0], inimigo[1], inimigo_imagem.get_width(), inimigo_imagem.get_height()).colliderect((bala[0], bala[1], bala_imagem.get_width(), bala_imagem.get_height()))]
        if colisoes:
            pontuacao += 10 * len(colisoes)
            for colisao in colisoes:
                balas.remove(colisao)
            inimigos.remove(inimigo)

    # Atualização da vida do personagem
    for inimigo in inimigos:
        if pygame.Rect(personagem_imagem.get_rect(center=personagem_rect.center)).colliderect(inimigo_imagem.get_rect(center=(inimigo[0], inimigo[1])):
            vida_personagem -= 10

    # Recarrega balas ao pressionar "R"
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_r]:
        balas_disponiveis = 12

    # Limpeza da tela
    janela.blit(fundo, (0, 0))

    # Desenho dos elementos
    janela.blit(personagem_rotacionado, personagem_rect.topleft)
    for inimigo in inimigos:
        janela.blit(inimigo_imagem, (inimigo[0], inimigo[1]))
    for bala in balas:
        janela.blit(bala_imagem, (bala[0], bala[1]))

    # Exibição da pontuação
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (0, 0, 0))
    janela.blit(texto_pontuacao, (10, 10))

    # Exibição das balas disponíveis
    texto_balas = fonte.render(f'Balas: {balas_disponiveis}', True, (0, 0, 0))
    janela.blit(texto_balas, (10, 50))

    # Exibição da vida do personagem
    texto_vida = fonte.render(f'Vida: {vida_personagem}', True, (255, 0, 0))
    janela.blit(texto_vida, (10, 90))

    # Exibição do número da rodada
    texto_round = fonte.render(f'Rodada: {round_atual}', True, (0, 0, 0))
    janela.blit(texto_round, (10, 130))

    # Verificação do fim da rodada
    if not inimigos:
        iniciar_round()

    # Verificação do fim do jogo
    if vida_personagem <= 0:
        jogando = False

    # Atualização da tela
    pygame.display.flip()

# Encerramento do jogo
pygame.quit()
sys.exit()
