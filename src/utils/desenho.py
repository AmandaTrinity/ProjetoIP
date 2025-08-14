import pygame
from src.utils.constantes import VERMELHO, BRANCO, CINZA, AMARELO

def desenhar_texto(texto, fonte, cor, superficie, x, y, centro=False):
    """Desenha um objeto de texto na superfície."""
    objeto_texto = fonte.render(texto, True, cor)
    rect_texto = objeto_texto.get_rect()
    if centro:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    superficie.blit(objeto_texto, rect_texto)

def desenhar_botao_mudo(surface, rect, muted):
    """Desenha o ícone de mudo/som."""
    cor_icone = VERMELHO if muted else BRANCO
    pygame.draw.rect(surface, CINZA, rect)
    pygame.draw.rect(surface, BRANCO, rect, 2)
    p, q = rect.centerx - 10, rect.centery
    pygame.draw.polygon(surface, cor_icone, [(p, q-7), (p+5, q-7), (p+13, q-12), (p+13, q+12), (p+5, q+7), (p, q+7)])
    if muted:
        pygame.draw.line(surface, VERMELHO, rect.topleft, rect.bottomright, 3)

def desenhar_hud(tela, hud_vars, professor, fase, tempo_restante, fontes, icones, rect_botao_mudo, som_mutado):
    """Desenha toda a barra lateral (HUD)."""
    from src.utils.constantes import LARGURA_TELA, ALTURA_TELA, LARGURA_BARRA_LATERAL, AZUL_CIN, BRANCO, AMARELO, VERMELHO, PRETO

    superficie_barra_lateral = pygame.Surface((LARGURA_BARRA_LATERAL, ALTURA_TELA))
    superficie_barra_lateral.fill(AZUL_CIN)

    desenhar_botao_mudo(superficie_barra_lateral, rect_botao_mudo, som_mutado)

    # Título da Fase
    desenhar_texto(f"FASE {fase}", fontes['pequena'], AMARELO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 20, True)
    desenhar_texto("COLETÁVEIS", fontes['pequena'], BRANCO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 60, True)

    # Ícones e timers
    y_icone, x_icone1, x_icone2 = 100, 45, 155
    tempo_atual = pygame.time.get_ticks()

    icones['sombrinha'].set_alpha(255 if hud_vars['sombrinha_coletada'] else 128)
    superficie_barra_lateral.blit(icones['sombrinha'], icones['sombrinha'].get_rect(center=(x_icone1, y_icone + 20)))
    if professor.tempo_boost > tempo_atual:
        desenhar_texto(f"{(professor.tempo_boost - tempo_atual) / 1000:.1f}s", fontes['mini'], VERMELHO, superficie_barra_lateral, x_icone1, y_icone + 50, True)

    icones['mascara'].set_alpha(255 if hud_vars['mascara_coletada'] else 128)
    superficie_barra_lateral.blit(icones['mascara'], icones['mascara'].get_rect(center=(x_icone2, y_icone + 20)))
    if professor.tempo_invisivel > tempo_atual:
        desenhar_texto(f"{(professor.tempo_invisivel - tempo_atual) / 1000:.1f}s", fontes['mini'], VERMELHO, superficie_barra_lateral, x_icone2, y_icone + 50, True)

    icones['pitu'].set_alpha(255 if hud_vars['pitu_coletada'] else 128)
    superficie_barra_lateral.blit(icones['pitu'], icones['pitu'].get_rect(center=(LARGURA_BARRA_LATERAL / 2, y_icone + 100)))
    if professor.tempo_drunk > tempo_atual:
        desenhar_texto(f"{(professor.tempo_drunk - tempo_atual) / 1000:.1f}s", fontes['mini'], VERMELHO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, y_icone + 130, True)

    # Contador de Coletáveis
    coletaveis_coletados = sum([
        hud_vars.get('sombrinha_coletada', False),
        hud_vars.get('mascara_coletada', False),
        hud_vars.get('pitu_coletada', False)
    ])
    desenhar_texto("COLETADOS", fontes['pequena'], BRANCO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 260, True)
    desenhar_texto(f"{coletaveis_coletados} / 3", fontes['media'], AMARELO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 295, True)

    # Tempo restante (reposicionado)
    desenhar_texto("TEMPO", fontes['pequena'], BRANCO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 350, True)
    cor_tempo = VERMELHO if tempo_restante <= 10 else BRANCO
    desenhar_texto(f"{int(tempo_restante)}", fontes['grande'], cor_tempo, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 380, True)

    # Caixa de Mensagens
    pygame.draw.rect(superficie_barra_lateral, PRETO, (10, 400, 180, 180))
    pygame.draw.rect(superficie_barra_lateral, BRANCO, (10, 400, 180, 180), 2)
    desenhar_texto("Mensagens", fontes['pequena'], AMARELO, superficie_barra_lateral, LARGURA_BARRA_LATERAL / 2, 415, True)
    y_offset = 440
    for msg in hud_vars.get('mensagens', []):
        desenhar_texto(msg, fontes['minuscula'], BRANCO, superficie_barra_lateral, 15, y_offset)
        y_offset += 15

    tela.blit(superficie_barra_lateral, (LARGURA_TELA, 0))