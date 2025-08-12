# Define a classe La ursa, que representa os obstáculos móveis (inimigos) no jogo.
import pygame
from src.utils.constantes import TAMANHO_BLOCO, VELOCIDADE_JOGADOR, DIRETORIO_IMAGENS
from src.utils.setup import carregar_animacao

class Laursa(pygame.sprite.Sprite):
    """Representa o obstáculo 'La Ursa' que se move verticalmente como um obstáculo."""
    def __init__(self, x, y):
        super().__init__()
        # Define o tamanho do sprite com base no tamanho do bloco do labirinto.
        tamanho_sprite = (TAMANHO_BLOCO, TAMANHO_BLOCO)
        
        # Variáveis para controlar a velocidade da animação.
        self.tempo_animacao = 0
        self.velocidade_animacao = 150
        
        # Carrega as animações de subida e descida do personagem.
        self.animacoes = {
            'descendo': carregar_animacao(DIRETORIO_IMAGENS, "laursafrente_", 4, tamanho_sprite),
            'subindo': carregar_animacao(DIRETORIO_IMAGENS, "laursasubindo_", 4, tamanho_sprite)
        }
        
        # Define o estado inicial da animação e da imagem.
        self.frame_atual = 0
        self.image = self.animacoes['descendo'][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
        # Controla a direção do movimento vertical (1 para baixo, -1 para cima).
        self.direcao = 1
        # Define a distância máxima que a LaUrsa se move a partir de sua posição inicial.
        self.movimento_range = 120
        # Armazena a posição Y inicial para calcular o alcance do movimento.
        self.pos_inicial_y = y

    def update(self, tempo_atual):
        """Atualiza a posição e a animação da LaUrsa a cada frame."""
        # Move a LaUrsa verticalmente. A velocidade é fixa em 2 pixels por frame.
        self.rect.y += self.direcao * 2
        
        # Verifica se a LaUrsa atingiu o limite superior ou inferior de seu movimento.
        if self.rect.y > self.pos_inicial_y + self.movimento_range or self.rect.y < self.pos_inicial_y:
            # Inverte a direção do movimento.
            self.direcao *= -1
            
        # Controla a troca de frames da animação com base no tempo.
        if tempo_atual - self.tempo_animacao > self.velocidade_animacao:
            self.tempo_animacao = tempo_atual
            # Seleciona a animação correta com base na direção do movimento.
            estado = 'descendo' if self.direcao == 1 else 'subindo'
            # Avança para o próximo frame, voltando ao início se chegar ao fim.
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[estado])
            self.image = self.animacoes[estado][self.frame_atual]
            # Atualiza a máscara de colisão para corresponder ao novo frame.
            self.mask = pygame.mask.from_surface(self.image)
