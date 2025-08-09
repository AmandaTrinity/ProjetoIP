import pygame
import os
from src.utils.constantes import *

class Aluno(pygame.sprite.Sprite):
    """Classe para os obstáculos que se movem."""
    def __init__(self, x, y):
        super().__init__()

        self.tempo_animacao = 0 #para temporização da animação
        self.velocidade_animacao = 150

        self.animacoes = {}
        try:
            laursa_descendo_lista = [] #Carrega animação descendo
            for i in range(4):
                nome_do_arquivo = f"laursafrente_{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                print(f"Tentando carregar: {caminho_completo}") 
                laursa_descendo = pygame.image.load(caminho_completo).convert_alpha()
                laursa_descendo = pygame.transform.scale(laursa_descendo, (40, 40))
                laursa_descendo_lista.append(laursa_descendo)

            self.animacoes['descendo'] = laursa_descendo_lista
            laursa_subindo_lista = []
            for i in range(4): #Carrega animação descendo
                nome_do_arquivo = f"laursasubindo_{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                print(f"Tentando carregar: {caminho_completo}") 
                laursa_subindo = pygame.image.load(caminho_completo).convert_alpha()
                laursa_subindo = pygame.transform.scale(laursa_subindo, (40, 40))
                laursa_subindo_lista.append(laursa_subindo)

            self.animacoes['subindo'] = laursa_subindo_lista
        except pygame.error as e: #caso não encontre as imagens
            print(f"Erro ao carregar imagens do osbtáculo: {e}. Usando Fallback")
            fallback_surface = pygame.Surface((TAMANHO_BLOCO - 10, TAMANHO_BLOCO - 10))
            fallback_surface.fill(CIANO)
            self.animacoes['descendo'] = [fallback_surface]
            self.animacoes['subindo'] = [fallback_surface]

        self.frame_atual = 0

        self.image = self.animacoes['descendo'][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image) #Também precisa colocar máscara nos obstáculos e afins
        
        self.direcao = 1
        self.movimento_range = 120 # O quanto ele se move para frente e para trás
        self.pos_inicial_y = y

    def update(self, tempo_atual):
        """Move a la ursa verticalmente."""
        self.rect.y += self.direcao * 2
        if self.rect.y > self.pos_inicial_y + self.movimento_range or self.rect.y < self.pos_inicial_y:
            self.direcao *= -1
        
        #Lógica da animação:
        if tempo_atual - self.tempo_animacao > self.velocidade_animacao:
            self.tempo_animacao = tempo_atual

            if self.direcao == 1: # Está descendo
                estado_animacao_atual = 'descendo'
            else: # Está subindo
                estado_animacao_atual = 'subindo'

            lista_de_frames_atual=self.animacoes[estado_animacao_atual]

            self.frame_atual = (self.frame_atual + 1) % len(lista_de_frames_atual)
            
            self.image = lista_de_frames_atual[self.frame_atual]
            self.mask = pygame.mask.from_surface(self.image)
