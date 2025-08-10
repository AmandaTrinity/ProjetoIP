import pygame
from src.utils.desenho import desenhar_texto
from src.utils.constantes import *

def tela_inicial(tela,fonte_grande,fonte_media,fonte_pequena, som_inicio):
    tela.fill(PRETO)
    desenhar_texto(TITULO_JOGO, fonte_grande, AMARELO, tela, LARGURA_TELA // 2, ALTURA_TELA // 4, True)
    desenhar_texto("Ajude o Prof. Stefan a chegar no Carnaval!", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
    desenhar_texto("Pressione ENTER para começar", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 3 / 4, True)
    desenhar_texto("ESC para sair do jogo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 3 / 4 + 40, True)
    if not pygame.mixer.get_busy(): #Verifica antes se não está tocando a música
        som_inicio.play(-1) #toca em loop

def tela_vitoria(tela,fonte_grande,fonte_media,fonte_pequena):
    tela.fill(VERDE)
    desenhar_texto("VOCÊ CONSEGUIU!", fonte_grande, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 3, True)
    desenhar_texto("RUMO AO CARNAVAL!", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
    desenhar_texto("Pressione ENTER para jogar de novo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 2 / 3, True)

def tela_derrota(tela,fonte_grande,fonte_media,fonte_pequena):
    tela.fill(VERMELHO)
    desenhar_texto("TEMPO ESGOTADO!", fonte_grande, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 3, True)
    desenhar_texto("Mais um ano no CIn...", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
    desenhar_texto("Pressione ENTER para tentar de novo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 2 / 3, True)