# src/sprites.py
import pygame
import os
import random  # <- ESTA É A LINHA QUE FALTAVA
from settings import *
from utils import carregar_animacao

# --- Classes de Sprites ---
class Professor(pygame.sprite.Sprite):
    def __init__(self, x, y, som_andando, sons_efeitos):
        super().__init__()
        tamanho_sprite = (TAMANHO_BLOCO, TAMANHO_BLOCO)

        self.animacoes = {
            'normal direita': carregar_animacao(DIRETORIO_IMAGENS, "stefan_direita", 4, tamanho_sprite),
            'normal esquerda': carregar_animacao(DIRETORIO_IMAGENS, "stefan_esquerda", 4, tamanho_sprite),
            'vampiro direita': carregar_animacao(DIRETORIO_IMAGENS, "stefanvampiro_direita", 4, tamanho_sprite),
            'vampiro esquerda': carregar_animacao(DIRETORIO_IMAGENS, "stefanvampiroesqueda_", 4, tamanho_sprite)
        }
        self.parado = {
            'normal direita': self.animacoes['normal direita'][0],
            'normal esquerda': self.animacoes['normal esquerda'][0],
            'vampiro direita': self.animacoes['vampiro direita'][0],
            'vampiro esquerda': self.animacoes['vampiro esquerda'][0]
        }
        
        self.tipo = 'normal '
        self.direcao = 'direita'
        self.image = self.parado[self.tipo + self.direcao]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 32, 38)
        self.hitbox.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        
        self.frame_atual = 0
        self.tempo_animacao = 0
        self.velocidade_animacao = 100
        self.velocidade = VELOCIDADE_JOGADOR
        self.itens_coletados = []
        
        # Efeitos de status
        self.invisivel = False
        self.drunk = False
        self.tempo_boost = 0
        self.tempo_invisivel = 0
        self.tempo_drunk = 0
        
        # Controle de som
        self.som_andando = som_andando
        self.som_sombrinha = sons_efeitos['sombrinha']
        self.canal_passos = pygame.mixer.Channel(2)
        self.canal_efeitos = pygame.mixer.Channel(1)
        self.som_andando_tocando = False

    def mover(self, desloc_x, desloc_y, paredes):
        # Primeiro, movemos e verificamos a colisão no eixo X (horizontal)
        self.hitbox.x += desloc_x * self.velocidade
        self.rect.centerx = self.hitbox.centerx  # Sincroniza o rect com o hitbox para a verificação
        
        # Verifica se há colisões após o movimento horizontal
        colisoes = pygame.sprite.spritecollide(self, paredes, False, pygame.sprite.collide_mask)
        if colisoes:
            # Se colidiu, voltamos à posição X anterior ao movimento
            self.hitbox.x -= desloc_x * self.velocidade
            self.rect.centerx = self.hitbox.centerx

        # Agora, independentemente do que aconteceu em X, fazemos o mesmo para o eixo Y (vertical)
        self.hitbox.y += desloc_y * self.velocidade
        self.rect.centery = self.hitbox.centery  # Sincroniza o rect com o hitbox para a verificação

        # Verifica se há colisões após o movimento vertical
        colisoes = pygame.sprite.spritecollide(self, paredes, False, pygame.sprite.collide_mask)
        if colisoes:
            # Se colidiu, voltamos à posição Y anterior ao movimento
            self.hitbox.y -= desloc_y * self.velocidade
            self.rect.centery = self.hitbox.centery

        # --- Finalização ---
        # A posição final do hitbox (e do rect) está agora correta, permitindo o deslize.
        
        personagem_se_moveu = (desloc_x != 0 or desloc_y != 0)

        # Atualiza a direção do sprite com base na intenção de movimento horizontal
        if desloc_x > 0:
            self.direcao = 'direita'
        elif desloc_x < 0:
            self.direcao = 'esquerda'

        return personagem_se_moveu

    def update(self, tempo_atual, deve_animar):
        # Controle do som de passos
        if deve_animar and not self.som_andando_tocando:
            self.canal_passos.play(self.som_andando, -1)
            self.som_andando_tocando = True
        elif not deve_animar and self.som_andando_tocando:
            self.canal_passos.stop()
            self.som_andando_tocando = False

        # Animação
        estado_animacao = self.tipo + self.direcao
        if deve_animar:
            if tempo_atual - self.tempo_animacao > self.velocidade_animacao:
                self.tempo_animacao = tempo_atual
                lista_frames = self.animacoes[estado_animacao]
                self.frame_atual = (self.frame_atual + 1) % len(lista_frames)
                self.image = lista_frames[self.frame_atual]
        else:
            self.image = self.parado[estado_animacao]
            self.frame_atual = 0
        
        # Timers de power-up
        if self.tempo_boost > 0 and tempo_atual > self.tempo_boost:
            self.velocidade = VELOCIDADE_JOGADOR
            self.tempo_boost = 0
            self.canal_efeitos.stop()
            pygame.mixer.Channel(0).unpause()

        if self.tempo_invisivel > 0 and tempo_atual > self.tempo_invisivel:
            self.invisivel = False
            self.tempo_invisivel = 0
            self.tipo = 'normal '
            self.image = self.parado[self.tipo + self.direcao]

        if self.tempo_drunk > 0 and tempo_atual > self.tempo_drunk:
            self.drunk = False
            self.tempo_drunk = 0

        self.image.set_alpha(128 if self.invisivel else 255)
        self.rect.center = self.hitbox.center

    def coletar_item(self, item, hud_vars):
        if item.nome not in self.itens_coletados:
            self.itens_coletados.append(item.nome)
            item.aplicar_efeito(self)
            item.kill()

            # Atualiza HUD
            if item.nome == "Sombrinha de Frevo":
                hud_vars['sombrinha_coletada'] = True
                hud_vars['mensagens'].append("Velocidade aumentada!")
            elif item.nome == "Garrafa de Pitú":
                hud_vars['pitu_coletada'] = True
                hud_vars['mensagens'].append("Controles invertidos!")
            elif item.nome == "Máscara de Carnaval":
                hud_vars['mascara_coletada'] = True
                hud_vars['mensagens'].append("Você está invisível!")
            
            if len(hud_vars['mensagens']) > 5:
                hud_vars['mensagens'].pop(0)

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


class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y, lista_telhados):
        super().__init__()
        self.image = random.choice(lista_telhados)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


# --- Classes de Itens ---
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

class SombrinhaFrevo(Item):
    def __init__(self, pos):
        super().__init__("Sombrinha de Frevo", pos, 'sprite_sheetsombrinha.png', 3, 26, 26)
    
    def aplicar_efeito(self, professor):
        pygame.mixer.Channel(0).pause()
        professor.canal_efeitos.play(professor.som_sombrinha)
        professor.velocidade = VELOCIDADE_JOGADOR * 2
        professor.tempo_boost = pygame.time.get_ticks() + DURACAO_BOOST_MS

class GarrafaPitu(Item):
    def __init__(self, pos, duracao_ms):
        super().__init__("Garrafa de Pitú", pos, 'pitu.png', 2, 60, 190, 10, 32)
        self.duracao_ms = duracao_ms
    
    def aplicar_efeito(self, professor):
        professor.drunk = True
        professor.tempo_drunk = pygame.time.get_ticks() + self.duracao_ms

class FantasiaCarnaval(Item):
    def __init__(self, pos):
        super().__init__("Máscara de Carnaval", pos, 'FantasiaVampiro 19x25.png', 1, 19, 25)
    
    def aplicar_efeito(self, professor):
        professor.tipo = 'vampiro '
        professor.invisivel = True
        professor.tempo_invisivel = pygame.time.get_ticks() + DURACAO_INVISIBILIDADE_MS