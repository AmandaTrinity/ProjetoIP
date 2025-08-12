# src/utils.py
import pygame
import os
from src.utils.constantes import VERMELHO

def carregar_animacao(caminho_base, prefixo_arquivo, num_frames, novo_tamanho):
    """Carrega uma sequência de imagens e a retorna como uma lista de surfaces."""
    frames = []
    for i in range(num_frames):
        nome_arquivo = f"{prefixo_arquivo}{i}.png"
        caminho_completo = os.path.join(caminho_base, nome_arquivo)
        try:
            imagem = pygame.image.load(caminho_completo).convert_alpha()
            frames.append(pygame.transform.scale(imagem, novo_tamanho))
        except pygame.error as e:
            print(f"Erro ao carregar frame '{caminho_completo}': {e}")
            fallback_surface = pygame.Surface(novo_tamanho)
            fallback_surface.fill(VERMELHO)
            frames.append(fallback_surface)
    return frames

class SomFalso:
    """Classe substituta para sons, caso o carregamento falhe."""
    def play(self, *args): pass
    def stop(self): pass
    def set_volume(self, v): pass