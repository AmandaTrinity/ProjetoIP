import pygame
import sys
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

#Lida com os eventos nas telas de vitória e derrota, retornando o novo estado
def lidar_eventos_fim_de_jogo(estado_atual):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return "TELA_INICIAL"
    # Mantém o estado se nenhuma ação relevante for tomada
    return estado_atual