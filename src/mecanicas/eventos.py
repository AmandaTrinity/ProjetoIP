import pygame
import sys
from src.utils.audio import toggle_mute
from src.utils.constantes import LARGURA_TELA

def processar_eventos(nome_estado_atual, config_audio, botoes=None):
    """
    Processa todos os eventos de input (teclado, mouse, fechar janela)
    e retorna um dicionário com os comandos para o loop principal.
    """
    comandos_usuario = {'acao': None, 'som_mutado': config_audio['som_mutado'],
                        'direcao_x': 0, 'direcao_y': 0,}

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Eventos de clique do mouse (para o botão de mudo)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicao_mouse = evento.pos

            # Lógica para o botão de iniciar jogo (VERSÃO FINAL)
            if nome_estado_atual == "TELA_INICIAL" and botoes:

                if 'iniciar' in botoes and botoes['iniciar'].verificar_input(posicao_mouse):
                    comandos_usuario['acao'] = 'INICIAR_JOGO'
                    return comandos_usuario

                # ADIÇÃO: Se o clique foi no botão de menu...
                if 'menu' in botoes and botoes['menu'].verificar_input(posicao_mouse):
                    comandos_usuario['acao'] = 'ABRIR_MENU'
                    return comandos_usuario
                
            if nome_estado_atual in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"] and botoes:
                if 'reiniciar' in botoes and botoes['reiniciar'].verificar_input(posicao_mouse):
                    comandos_usuario['acao'] = 'VOLTAR_MENU'
                    return comandos_usuario
                
            # Determina qual rect do botão de mudo está ativo (o do menu ou o da HUD)
            if nome_estado_atual != "JOGANDO":
                botao_mudo_rect = config_audio['rect_menu']
            else:
                hud_rect = config_audio['rect_hud']
                botao_mudo_rect = pygame.Rect(LARGURA_TELA + hud_rect.x, hud_rect.y, hud_rect.width, hud_rect.height)
            
            if botao_mudo_rect.collidepoint(evento.pos):
                comandos_usuario['som_mutado'] = toggle_mute(comandos_usuario['som_mutado'])

        # Eventos de teclado
        if evento.type == pygame.KEYDOWN:
            if nome_estado_atual == "TELA_MENU":
                if evento.key == pygame.K_ESCAPE:
                    comandos_usuario['acao'] = 'VOLTAR_MENU' # Fecha o menu
                elif evento.key == pygame.K_RETURN:
                    comandos_usuario['acao'] = 'RESETAR_PONTUACAO'
            
            
            else: # Lógica para os outros estados
                if evento.key == pygame.K_m:
                    comandos_usuario['som_mutado'] = toggle_mute(comandos_usuario['som_mutado'])
                elif evento.key == pygame.K_ESCAPE:
                    comandos_usuario['acao'] = 'VOLTAR_MENU'
                elif evento.key == pygame.K_r and nome_estado_atual == "TELA_INICIAL":
                    comandos_usuario['acao'] = 'ABRIR_MENU'
                elif evento.key == pygame.K_RETURN:
                    if nome_estado_atual == "TELA_INICIAL":
                        comandos_usuario['acao'] = 'INICIAR_JOGO'
                    elif nome_estado_atual in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"]:
                        comandos_usuario['acao'] = 'VOLTAR_MENU'

    # Captura de movimento contínuo (fora do loop de eventos)
    teclas_pressionadas = pygame.key.get_pressed()
    comandos_usuario['direcao_x'] = (teclas_pressionadas[pygame.K_RIGHT] or teclas_pressionadas[pygame.K_d]) - (teclas_pressionadas[pygame.K_LEFT] or teclas_pressionadas[pygame.K_a])
    comandos_usuario['direcao_y'] = (teclas_pressionadas[pygame.K_DOWN] or teclas_pressionadas[pygame.K_s]) - (teclas_pressionadas[pygame.K_UP] or teclas_pressionadas[pygame.K_w])

    return comandos_usuario