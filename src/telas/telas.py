# src/utils/telas.py
import pygame
from src.utils.constantes import *
from src.utils.desenho import desenhar_texto, desenhar_botao_mudo

def desenhar_tela_inicial(tela, recursos, som_mutado, rect_botao_mudo, botao_iniciar, botao_menu):
    # desenha todos os elementos da tela inicial
    tela.blit(recursos['fundo_tela_inicial'], (0, 0))
    if som_mutado:
        # Se o som estiver mudo, desenha o ícone de som desligado
        tela.blit(recursos['icones_som']['mudo'], rect_botao_mudo)
    else:
        # Se o som estiver ligado, desenha o ícone de som ligado
        tela.blit(recursos['icones_som']['ligado'], rect_botao_mudo)
    
    posicao_mouse = pygame.mouse.get_pos()
    
    botao_iniciar.atualizar_feedback(posicao_mouse)
    botao_iniciar.desenhar(tela)

    botao_menu.atualizar_feedback(posicao_mouse)
    botao_menu.desenhar(tela)

def exibir_tela_final(tela, cor, msg1, msg2, recursos, rect_botao_mudo, som_mutado, tempo_partida=None):
    """Desenha uma tela genérica de fim de jogo."""
    tela.fill(cor)
    largura_total = tela.get_width()
    altura_total = tela.get_height()

    desenhar_texto(msg1, recursos['fontes']['grande'], BRANCO, tela, largura_total // 2, altura_total // 3, True)
    desenhar_texto(msg2, recursos['fontes']['media'], BRANCO, tela, largura_total // 2, altura_total // 2, True)

    if tempo_partida is not None:
        texto_tempo = f"Seu tempo: {tempo_partida:.2f} segundos"
        desenhar_texto(texto_tempo, recursos['fontes']['pequena'], AMARELO, tela, largura_total // 2, altura_total * 2 // 3, True)

    desenhar_texto("Pressione ENTER para voltar", recursos['fontes']['pequena'], BRANCO, tela, largura_total // 2, altura_total * 5 // 6, True)
    if som_mutado:
        # Se o som estiver mudo, desenha o ícone de som desligado
        tela.blit(recursos['icones_som']['mudo'], rect_botao_mudo)
    else:
        # Se o som estiver ligado, desenha o ícone de som ligado
        tela.blit(recursos['icones_som']['ligado'], rect_botao_mudo)

# Em src/telas/telas.py

# Em src/telas/telas.py

def desenhar_menu_popup(tela, recursos, melhores_tempos):
    """Desenha o pop-up do menu com o texto mais 'junto' e centralizado no estandarte."""
    
    # --- FUNDO DO MENU ---
    # Esta parte continua igual, desenhando o estandarte no centro.
    fundo_menu_img = recursos['fundo_estandarte']
    pos_x = ((LARGURA_TOTAL - fundo_menu_img.get_width()) / 2) + 22
    pos_y = (ALTURA_TELA - fundo_menu_img.get_height()) / 2
    tela.blit(fundo_menu_img, (pos_x, pos_y))

    centro_x_menu = pos_x + fundo_menu_img.get_width() / 2
    
    # --- INSTRUÇÕES ---
    # Posição Y inicial. Aumentei para o texto começar mais para baixo, dentro da área vermelha.
    y_atual = pos_y + 205
    desenhar_texto("INSTRUÇÕES", recursos['fontes']['pequena'], AMARELO, tela, centro_x_menu, y_atual, True)
    
    y_atual += 40 # Diminuí o espaçamento para a próxima linha
    desenhar_texto("Use W, A, S, D", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    y_atual += 20
    desenhar_texto("para se mover", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    y_atual += 50 # Espaçamento entre linhas da mesma seção
    desenhar_texto("Colete os 3 itens", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    y_atual += 20
    desenhar_texto("para abrir a saída", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    y_atual += 40
    desenhar_texto("Pressione R para", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    y_atual += 20
    desenhar_texto("resetar o ranking", recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_atual, True)

    # --- RANKING ---
    y_atual += 40 # Espaço maior entre as seções "Instruções" e "Ranking"
    
    desenhar_texto("RANKING", recursos['fontes']['media'], AMARELO, tela, centro_x_menu, y_atual, True)
    
    y_ranking_lista = y_atual + 40
    for i, tempo in enumerate(melhores_tempos):
        texto_tempo = f"{i+1}. {tempo:.2f}s" if tempo != float('inf') else f"{i+1}. --"
        desenhar_texto(texto_tempo, recursos['fontes']['pequena'], BRANCO, tela, centro_x_menu, y_ranking_lista + (i * 30), True)

    # --- OPÇÕES DE AÇÃO ---
    y_acoes = pos_y + fundo_menu_img.get_height() - 260 # Subi um pouco para não ficar em cima das fitas
    desenhar_texto("FECHAR", recursos['fontes']['mini'], BRANCO, tela, centro_x_menu, y_acoes, True)

    y_acoes = pos_y + fundo_menu_img.get_height() - 240 # Subi um pouco para não ficar em cima das fitas
    desenhar_texto("(ESC)", recursos['fontes']['mini'], BRANCO, tela, centro_x_menu, y_acoes, True)