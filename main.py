import pygame
import random

# nossos braches
from config import *
from jogador import Jogador
from coletavel import Moeda, Pocao

# iniciar os recursos do pygame
pygame.init() 

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("GAME ON")
relogio = pygame.time.Clock()

pontuacao = 0
fonte = pygame.font.Font(None, 36)

# criação de objetos
jogador = Jogador()
moeda = Moeda()
pocao = Pocao()

ON = True
while ON:
    relogio.tick(69)
    
    for evento in pygame.event.get():

        if evento.type ==  pygame.QUIT:
            ON = False

    # quais teclas estao pressionadas agora?
    teclas = pygame.key.get_pressed()

    # chamar a função durante o jogo
    jogador.movimentos(teclas)

    # lógica de colisão jogador x cooletável
    # se a colisao for true, o jogador tocou no coletável
    if jogador.rect.colliderect(moeda.rect):
        pontuacao += 1
        moeda.respawn() # some e aparece em outro lugar
        print(f"Coletou Moeda! Pontuação atual: {pontuacao}")
    
    if jogador.rect.colliderect(pocao.rect):
        pontuacao += 1
        pocao.respawn() # some e aparece em outro lugar
        print(f"Coletou Poção! Pontuação atual: {pontuacao}")

    tela.fill((preto)) # pinta a tela de preto?
    tela.blit(jogador.image, jogador.rect) # desenha o jogador na tela
    tela.blit(moeda.image, moeda.rect)
    tela.blit(pocao.image, pocao.rect)
    
    pygame.display.flip()
    # .blit() = "copiar os pixels" da imagem do jogador para a tela,
    # na posição definida pelo retângulo do jogador.

    # requisito: mostrar pontuacao na tela?
    # rendezizar o texto -> criar superfícia com texto desenhado
    texto_surface = fonte.render(f"Pontos: {pontuacao}", True, branco)
    # desenhar a supercifie na tele
    tela.blit(texto_surface, (10,10))

    pygame.display.flip() # atualiza o que fizemos e mostra na tela

pygame.quit()