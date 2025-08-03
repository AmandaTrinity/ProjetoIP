import pygame
import random

# nossos braches
from config import *
from jogador import Jogador
from coletavel import Moeda, Pocao
from camera import Camera
from interacao import PontoDeInteresse


# iniciar os recursos do pygame
pygame.init() 

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("GAME ON")
relogio = pygame.time.Clock()

mapa_img = pygame.image.load('asset/SALVAPFV.jpg').convert()
mapa_rect = mapa_img.get_rect()    

pontuacao = 0
fonte = pygame.font.Font(None, 36)

todos_os_sprites = pygame.sprite.Group()

# criação de objetos
jogador = Jogador()
ponto_cin = PontoDeInteresse(400,300)
moeda = None # ainda nao xiste

todos_os_sprites.add(jogador, ponto_cin)

camera = Camera(mapa_rect.width, mapa_rect.height)

estado_jogo = ESTADO_EXPLORANDO

ON = True
while ON:
    relogio.tick(60)
    
    for evento in pygame.event.get():

        if evento.type ==  pygame.QUIT:
            ON = False

        if estado_jogo == ESTADO_EXPLORANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    if jogador.rect.colliderect(ponto_cin.rect):
                        print("Transição para o mini-game do CIn!")
                        # MUDANÇA PRINCIPAL: Em vez de criar a moeda, MUDAMOS O ESTADO DO JOGO.
                        estado_jogo = ESTADO_MINIGAME_CIN
        
        elif estado_jogo == ESTADO_MINIGAME_CIN:
            if evento.type == pygame.KEYDOWN:
                # NOVO: Criamos uma forma de "vencer" o minigame e voltar
                if evento.key == pygame.K_q: # Usaremos 'Q' para simular a vitória
                    print("Mini-game concluído! A Moeda apareceu no mapa!")
                    moeda = Moeda() # A moeda é criada como recompensa
                    todos_os_sprites.add(moeda)
                    estado_jogo = ESTADO_EXPLORANDO # Voltamos para o estado de exploração

    if estado_jogo == ESTADO_EXPLORANDO:
        teclas = pygame.key.get_pressed()
        jogador.movimentos(teclas)
        camera.update(jogador.rect)

        if moeda is not None and jogador.rect.colliderect(moeda.rect):
            print("Moeda coletada!")
            moeda.kill()
            moeda = None # A moeda foi coletada e não existe mais
        
        # Desenho do mundo de exploração
        tela.fill(preto)
        tela.blit(mapa_img, camera.apply(mapa_rect))
        for sprite in todos_os_sprites:
            tela.blit(sprite.image, camera.apply(sprite.rect))
        
        # Aqui podemos adicionar o placar dos itens coletados no futuro

    elif estado_jogo == ESTADO_MINIGAME_CIN:
        # Desenho da tela do mini-game (por enquanto, uma tela simples)
        tela.fill(preto)
        texto_minigame = fonte.render("Você está no mini-game do CIn!", True, branco)
        texto_instrucao = fonte.render("Pressione Q para vencer e voltar ao mapa.", True, branco)
        tela.blit(texto_minigame, (150, 250))
        tela.blit(texto_instrucao, (100, 300))

    pygame.display.flip() # atualiza o que fizemos e mostra na tela

pygame.quit()