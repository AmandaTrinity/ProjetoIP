import os
import pygame
from src.utils.constantes import SONS_DIR

#Carregando músicas
som_inicio = pygame.mixer.Sound(os.path.join(SONS_DIR, 'musica_inicio.mp3'))
som_inicio.set_volume(0.7)

som_jogo = pygame.mixer.Sound(os.path.join(SONS_DIR, 'musica_jogo.mp3'))
som_jogo.set_volume(0.4)

try:
    som_andando = pygame.mixer.Sound(os.path.join(SONS_DIR, 'andando.mp3'))
    som_andando.set_volume(1.0)

    som_sombrinha = pygame.mixer.Sound(os.path.join(SONS_DIR, 'som_sombrinha.wav'))
    som_sombrinha.set_volume(0.8)
    print("Efeitos sonoros carregados")
except pygame.error as e:
    print(f"Erro ao carregar efeitos sonoros: {e}.")
    class SomFalso: #Cria sons falsos, apenas para o jogo não quebrar
        def play(self, *args): pass
        def stop(self): pass
    som_andando = SomFalso()
    som_sombrinha = SomFalso ()