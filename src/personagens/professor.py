import pygame
from src.utils.constantes import TAMANHO_BLOCO, VELOCIDADE_JOGADOR, DIRETORIO_IMAGENS
from src.utils.setup import carregar_animacao
from src.mecanicas.movimento import mover_personagem

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
        """Delega a lógica de movimento para o módulo especializado."""
        return mover_personagem(self, desloc_x, desloc_y, paredes)

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