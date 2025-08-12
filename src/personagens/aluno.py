import pygame
from src.utils.constantes import TAMANHO_BLOCO, VELOCIDADE_JOGADOR, DIRETORIO_IMAGENS
from src.utils.setup import carregar_animacao

class Aluno(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tamanho_sprite = (TAMANHO_BLOCO, TAMANHO_BLOCO)
        self.tempo_animacao = 0
        self.velocidade_animacao = 150
        
        self.animacoes = {
            'descendo': carregar_animacao(DIRETORIO_IMAGENS, "laursafrente_", 4, tamanho_sprite),
            'subindo': carregar_animacao(DIRETORIO_IMAGENS, "laursasubindo_", 4, tamanho_sprite)
        }
        self.frame_atual = 0
        self.image = self.animacoes['descendo'][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
        self.direcao = 1
        self.movimento_range = 120
        self.pos_inicial_y = y

    def update(self, tempo_atual):
        self.rect.y += self.direcao * 2
        if self.rect.y > self.pos_inicial_y + self.movimento_range or self.rect.y < self.pos_inicial_y:
            self.direcao *= -1
            
        if tempo_atual - self.tempo_animacao > self.velocidade_animacao:
            self.tempo_animacao = tempo_atual
            estado = 'descendo' if self.direcao == 1 else 'subindo'
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[estado])
            self.image = self.animacoes[estado][self.frame_atual]
            self.mask = pygame.mask.from_surface(self.image)
