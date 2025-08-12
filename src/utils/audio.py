import pygame
from src.utils.constantes import VOLUMES_PADRAO

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