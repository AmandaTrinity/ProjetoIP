import pygame
import os
from src.utils.constantes import VOLUMES_PADRAO, DIRETORIO_SONS

def toggle_mute(muted):
    """Ativa ou desativa o som de todos os canais."""
    muted = not muted
    volume_fator = 0 if muted else 1
    pygame.mixer.Channel(0).set_volume(VOLUMES_PADRAO['musica'] * volume_fator)
    pygame.mixer.Channel(1).set_volume(VOLUMES_PADRAO['efeitos'] * volume_fator)
    pygame.mixer.Channel(2).set_volume(VOLUMES_PADRAO['passos'] * volume_fator)
    return muted

class SomFalso:
    """Classe substituta para sons, caso o carregamento falhe."""
    def play(self, *args): pass
    def stop(self): pass
    def set_volume(self, v): pass

def carregar_sons():
    """Carrega todos os arquivos de áudio do jogo."""
    try:
        sons = {
            'inicio': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'musica_inicio.mp3')),
            'jogo': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'musica_jogo.mp3')),
            'andando': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'andando.mp3')),
            'sombrinha': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'som_sombrinha.wav'))
        }
    except pygame.error:
        print("Aviso: Um ou mais sons não puderam ser carregados. Usando sons falsos.")
        sons = {k: SomFalso() for k in ['inicio', 'jogo', 'andando', 'sombrinha']}
    return sons
