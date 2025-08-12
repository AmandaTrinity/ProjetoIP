# src/utils/telas.py
import pygame
from src.utils.constantes import *
from src.utils.desenho import desenhar_texto, desenhar_botao_mudo

def desenhar_tela_inicial(tela, fontes, melhores_tempos, som_mutado, botao_mudo_rect_menu):
    """Desenha todos os elementos da tela inicial."""
    tela.fill(PRETO)
    desenhar_texto(TITULO_JOGO, fontes['grande'], AMARELO, tela, LARGURA_TOTAL / 2, ALTURA_TELA / 5, True)
    desenhar_texto("Pressione ENTER para começar", fontes['pequena'], BRANCO, tela, LARGURA_TOTAL / 2, ALTURA_TELA * 3.5 / 5, True)
    desenhar_texto("Pressione ESC para voltar ao MENU", fontes['mini'], CINZA, tela, LARGURA_TOTAL / 2, ALTURA_TELA * 4.0 / 5, True)
    desenhar_botao_mudo(tela, botao_mudo_rect_menu, som_mutado)
    desenhar_texto("Tempo mais rápido", fontes['media'], AMARELO, tela, LARGURA_TOTAL / 2, ALTURA_TELA / 2 - 40, True)
    for i, tempo in enumerate(melhores_tempos):
        texto_tempo = f"{i+1}. {tempo:.2f}s" if tempo != float('inf') else f"{i+1}. --"
        desenhar_texto(texto_tempo, fontes['pequena'], BRANCO, tela, LARGURA_TOTAL / 2, ALTURA_TELA / 2 + (i * 30), True)
    desenhar_texto("Pressione R para resetar o tempo", fontes['pequena'], VERMELHO, tela, LARGURA_TOTAL / 2, ALTURA_TELA * 4.5 / 5, True)

def exibir_tela_final(tela, cor, msg1, msg2, fontes, rect_botao_mudo, som_mutado, tempo_partida=None):
    """Desenha uma tela genérica de fim de jogo."""
    tela.fill(cor)
    largura_total = tela.get_width()
    altura_total = tela.get_height()

    desenhar_texto(msg1, fontes['grande'], BRANCO, tela, largura_total // 2, altura_total // 3, True)
    desenhar_texto(msg2, fontes['media'], BRANCO, tela, largura_total // 2, altura_total // 2, True)

    if tempo_partida is not None:
        texto_tempo = f"Seu tempo: {tempo_partida:.2f} segundos"
        desenhar_texto(texto_tempo, fontes['pequena'], AMARELO, tela, largura_total // 2, altura_total * 2 // 3, True)

    desenhar_texto("Pressione ENTER para voltar", fontes['pequena'], BRANCO, tela, largura_total // 2, altura_total * 5 // 6, True)
    desenhar_botao_mudo(tela, rect_botao_mudo, som_mutado)

def desenhar_tela_confirmacao_reset(tela, fontes):
    """Desenha o pop-up de confirmação para resetar o ranking."""
    # Desenha a caixa de diálogo por cima da tela existente
    popup_largura, popup_altura = 700, 200
    popup_rect = pygame.Rect((LARGURA_TOTAL - popup_largura) / 2, (ALTURA_TELA - popup_altura) / 2, popup_largura, popup_altura)
    pygame.draw.rect(tela, AZUL_CIN, popup_rect)
    pygame.draw.rect(tela, BRANCO, popup_rect, 3) # Borda

    desenhar_texto("Você tem certeza que deseja resetar o Ranking?", fontes['mini'], BRANCO, tela, popup_rect.centerx, popup_rect.centery - 30, True)
    desenhar_texto("Sim (ENTER) / Não (ESC)", fontes['pequena'], AMARELO, tela, popup_rect.centerx, popup_rect.centery + 30, True)