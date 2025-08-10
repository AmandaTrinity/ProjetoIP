import pygame
import os
from src.utils.constantes import TAMANHO_BLOCO,SPRITES_DIR

class Item(pygame.sprite.Sprite):
    """Classe base para todos os itens coletáveis."""
    def __init__(self, nome, pos, imagens, n_sprites, largura, altura, nova_largura=None, nova_altura=None):
        super().__init__()
        self.nome = nome
        self.image = pygame.Surface((TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2))
        self.rect = self.image.get_rect(center=pos)
        sprite_sheet = pygame.image.load(os.path.join(SPRITES_DIR, imagens)).convert_alpha()
        self.lista_sprites = []
        for i in range(n_sprites): # número de sprites
            sprite = sprite_sheet.subsurface((i * largura, 0), (largura, altura))
            if nova_altura != None and nova_largura != None:
                sprite = pygame.transform.scale(sprite, (nova_largura, nova_altura))
            self.lista_sprites.append(sprite)

        self.index_lista = 0

        # substituindo imagem placeholder
        self.image = self.lista_sprites[self.index_lista]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.index_lista += 0.15
        if self.index_lista >= len(self.lista_sprites):
            self.index_lista = 0
        self.image = self.lista_sprites[int(self.index_lista)]
        self.mask = pygame.mask.from_surface(self.image)

    def aplicar_efeito(self, professor):
        """Método a ser sobrescrito por cada item."""
        print(f"Item {self.nome} coletado!")
