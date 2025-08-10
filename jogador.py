import pygame
from config import *

# criando a classe JOGADOR -> molde

class Jogador(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__() # inicialização da classe mae spite

        # imagem do jogador (quadrado azul?)
        self.image = pygame.Surface((50,50))
        self.image.fill((0,0,255)) # pintando de azul?

        # pegar retangulo que representa posicao e tamanho?
        # sera usado para posicionar e desenhar o jogador?
        self.rect = self.image.get_rect()

        # definir a posicao incial do jogador no centro/baixo
        self.rect.centerx = 400
        self.rect.bottom = 600

        self.velocidade = 3 # atributo para guardar a velocidade

    def movimentos(self, teclas): # qual é o estado de todas as teclas do teclado?

        # já tem no dicionario essa convenção AWSD

        # esquerda?
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade # move retangulo pra esquerda
        
        # direita?
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade # move retangulo pra direita

        # cima
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade # move retangulo pra cima

        # baixo
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade # move retangulo pra baixo