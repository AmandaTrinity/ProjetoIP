# a câmera não é algo pronto na biblioteca pygame
# é preciso criar uma lógica pra ela
# a camera é um conjunto de calculos que dizem QUAL parte da imagem deve estar na tela

# QUANDO AWSD PRESSIONADO, NÃO É O JOGADOR QUE SE MOVE, É A IMAGEM

# ATUALIZAÇÃO: para que o pygame consiga gerir e desenhar vários objetos com uma CAMERA, eles precisam ser SPRITE
    #  um Sprite no Pygame é a representação base de qualquer objeto de jogo

import pygame
from config import *

class Camera:

    # pra criar uma camera, é preciso dizer o tamanho dela (tamanho da tela do jogo)
    # a posição (topleft) vai mudar para seguir o jogador
    def __init__(self, largura_mapa, altura_mapa):
        self.camera = pygame.Rect(0, 0, tela_largura, tela_altura)
        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa

    # em que entidade significa ququer objeto do jogo
    # calcular onde o retângulo de um objeto deve ser desenhado na tela
    # CONSIDERANDO O DESLOCAMENTO DA CAMERA
    # traducao de uma coordenada do mundo em uma coordenada da tela?
    def apply(self, entidade_rect):
        return entidade_rect.move(self.camera.topleft)

    # atualiza a posição da câmera para se centrar no alvo
    # alvo no caso é o jogador
    # esse metodo é chamado a cada momento no jogo
    def update(self, alvo_rect):

        # CALCULO: RETANGULO OBJETO NO MEIO DE TELA
        x = -alvo_rect.centerx + tela_largura // 2
        y = -alvo_rect.centery + tela_altura // 2

        # scrool nao pode mostrar áreas fora do mapa
        x = min(0, x)  # limite esquerdo
        y = min(0, y)  # limite superior
        x = max(-(self.largura_mapa - tela_largura), x)  # limite direito
        y = max(-(self.altura_mapa - tela_altura), y)  # limite inferior

        # atualiza a posição da câmera com os novos valores de x e y
        self.camera.topleft = (x, y)