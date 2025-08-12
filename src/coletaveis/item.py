import pygame
import os
from src.settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, nome, pos, img_path, n, w, h, new_w=None, new_h=None):
        super().__init__()
        self.nome = nome
        caminho_completo = os.path.join(DIRETORIO_IMAGENS, img_path)
        try:
            sprite_sheet = pygame.image.load(caminho_completo).convert_alpha()
        except pygame.error:
            print(f"AVISO: Não foi possível carregar o item '{caminho_completo}'. Usando fallback.")
            sprite_sheet = pygame.Surface((w, h), pygame.SRCALPHA)
        
        self.lista_sprites = []
        for i in range(n):
            sprite = sprite_sheet.subsurface((i * w, 0), (w, h))
            if new_w and new_h:
                sprite = pygame.transform.scale(sprite, (new_w, new_h))
            self.lista_sprites.append(sprite)
            
        self.index_lista = 0
        self.image = self.lista_sprites[self.index_lista]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.index_lista = (self.index_lista + 0.15) % len(self.lista_sprites)
        self.image = self.lista_sprites[int(self.index_lista)]

    def aplicar_efeito(self, professor):
        raise NotImplementedError
