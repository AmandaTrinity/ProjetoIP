# main.py
import pygame
import sys
import os
from src.utils.constantes import *
from src.utils.desenho import desenhar_hud, desenhar_texto
from src.mecanicas.level import setup_fase
from src.utils.audio import toggle_mute, carregar_sons
from src.telas.telas import desenhar_tela_inicial, exibir_tela_final, desenhar_tela_confirmacao_reset
from src.utils.pontuacao import carregar_melhores_tempos, salvar_melhores_tempos
from src.utils.setup import carregar_recursos_globais
from src.mecanicas.eventos import processar_eventos

def main():
    pygame.init()
    pygame.mixer.init()

    tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # --- CARREGAMENTO DE RECURSOS GLOBAIS ---
    recursos_visuais = carregar_recursos_globais()
    sons = carregar_sons()

    pygame.mixer.set_num_channels(3)
    canal_musica = pygame.mixer.Channel(0)
    
    # --- VARIÁVEIS DE ESTADO DO JOGO ---
    estado_som = {
        'som_mutado': False,
        'rect_hud': pygame.Rect(LARGURA_BARRA_LATERAL - 45, 10, 35, 30),
        'rect_menu': pygame.Rect(10, 10, 35, 30)
    }

    melhores_tempos = carregar_melhores_tempos()
    tempo_total_corrida = 0.0
    tempo_inicio_fase_atual = 0
    
    estado_jogo = "TELA_INICIAL"
    fase_atual = 1
    tempo_inicio_transicao = 0
    ponto_referencia_timer_regressivo = 0
    porta_animando = False
    porta_frame_atual = 0
    porta_ultimo_update = 0
    
    elementos_fase = {}

    # --- LOOP PRINCIPAL ---
    while True:
        tempo_atual = pygame.time.get_ticks()
        comandos_usuario = processar_eventos(estado_jogo, estado_som)
        estado_som['som_mutado'] = comandos_usuario['som_mutado']

        # --- ATUALIZAÇÃO DE ESTADO BASEADO NOS COMANDOS ---
        acao = comandos_usuario.get('acao')
        if acao == 'VOLTAR_MENU':
            canal_musica.stop(); pygame.mixer.Channel(2).stop()
            estado_jogo = "TELA_INICIAL"
        elif acao == 'INICIAR_JOGO':
            fase_atual = 1
            elementos_fase = setup_fase(fase_atual, recursos_visuais['lista_telhados'], sons)
            ponto_referencia_timer_regressivo = tempo_atual
            tempo_total_corrida = 0.0
            tempo_inicio_fase_atual = tempo_atual
            porta_animando, porta_frame_atual = False, 0
            canal_musica.stop()
            canal_musica.play(sons['jogo'], -1)
            estado_jogo = "JOGANDO"
        elif acao == 'CONFIRMAR_RESET':
            estado_jogo = "CONFIRMAR_RESET"
        elif acao == 'RESETAR_PONTUACAO':
            melhores_tempos = [float('inf'), float('inf')]
            salvar_melhores_tempos(melhores_tempos)
            estado_jogo = "TELA_INICIAL"
        elif acao == 'CANCELAR_RESET':
            estado_jogo = "TELA_INICIAL"
        
        # --- LÓGICA DE ESTADOS ---
        if estado_jogo == "TELA_INICIAL":
            if not canal_musica.get_busy():
                canal_musica.play(sons['inicio'], -1)
            desenhar_tela_inicial(tela, recursos_visuais['fontes'], melhores_tempos, estado_som['som_mutado'], estado_som['rect_menu'])

        ### NOVO ### - Estado para desenhar o pop-up de confirmação
        elif estado_jogo == "CONFIRMAR_RESET":
            # Primeiro, desenha a tela inicial por baixo para criar o efeito de pop-up
            desenhar_tela_inicial(tela, recursos_visuais['fontes'], melhores_tempos, estado_som['som_mutado'], estado_som['rect_menu'])
            desenhar_tela_confirmacao_reset(tela, recursos_visuais['fontes'])

        elif estado_jogo == "TRANSICAO_FASE":
            tela.fill(PRETO)
            desenhar_texto(f"FASE {fase_atual}", recursos_visuais['fontes']['grande'], BRANCO, tela, LARGURA_TOTAL / 2, ALTURA_TELA / 2, True)
            if tempo_atual - tempo_inicio_transicao > 3000:
                elementos_fase = setup_fase(fase_atual, recursos_visuais['lista_telhados'], sons)
                ponto_referencia_timer_regressivo = tempo_atual
                porta_animando, porta_frame_atual = False, 0
                estado_jogo = "JOGANDO"

        elif estado_jogo in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"]:
            mensagens_fim = {
                "VITORIA": (VERDE, "VOCÊ CONSEGUIU!", "RUMO AO CARNAVAL!"),
                "DERROTA": (VERMELHO, "TEMPO ESGOTADO!", "Mais um ano no CIn..."),
                "DERROTA_OBSTACULO": (VERMELHO, "GAME OVER!", "Você não sobreviveu à multidão.")
            }
            cor, mensagem_principal, mensagem_secundaria = mensagens_fim[estado_jogo]
            tempo_a_exibir = tempo_total_corrida if estado_jogo == "VITORIA" else None
            exibir_tela_final(tela, cor, mensagem_principal, mensagem_secundaria, recursos_visuais['fontes'], estado_som['rect_menu'], estado_som['som_mutado'], tempo_partida=tempo_a_exibir)

        elif estado_jogo == "JOGANDO":
            professor = elementos_fase['professor']
            deslocamento_x, deslocamento_y = comandos_usuario['direcao_x'], comandos_usuario['direcao_y']
            if professor.drunk: deslocamento_x, deslocamento_y = -deslocamento_x, -deslocamento_y
            
            personagem_se_moveu = professor.mover(deslocamento_x, deslocamento_y, elementos_fase['paredes'])
            professor.update(tempo_atual, personagem_se_moveu)
            elementos_fase['obstaculos'].update(tempo_atual)
            elementos_fase['itens'].update()

            for item in pygame.sprite.spritecollide(professor, elementos_fase['itens'], False, pygame.sprite.collide_mask):
                professor.coletar_item(item, elementos_fase['hud_vars'])
            
            if not professor.invisivel and pygame.sprite.spritecollide(professor, elementos_fase['obstaculos'], False, pygame.sprite.collide_mask):
                if fase_atual == 3:
                    canal_musica.stop(); pygame.mixer.Channel(2).stop(); estado_jogo = "DERROTA_OBSTACULO"
                else:
                    ponto_referencia_timer_regressivo -= 2000
                    professor.hitbox.x -= deslocamento_x * professor.velocidade * 4
                    professor.hitbox.y -= deslocamento_y * professor.velocidade * 4
            
            if len(professor.itens_coletados) == 3 and not porta_animando and porta_frame_atual == 0:
                porta_animando = True
                porta_ultimo_update = tempo_atual
            
            if porta_animando and tempo_atual - porta_ultimo_update > 200:
                porta_ultimo_update = tempo_atual
                porta_frame_atual = min(porta_frame_atual + 1, len(recursos_visuais['lista_sprites_porta']) - 1)
                if porta_frame_atual == len(recursos_visuais['lista_sprites_porta']) - 1:
                    porta_animando = False
            
            tempo_restante = TEMPO_TOTAL_JOGO - (tempo_atual - ponto_referencia_timer_regressivo) / 1000
            if tempo_restante <= 0:
                canal_musica.stop(); pygame.mixer.Channel(2).stop(); estado_jogo = "DERROTA"
            
            if len(professor.itens_coletados) == 3 and porta_frame_atual == 3 and professor.hitbox.colliderect(elementos_fase['pos_saida']):
                pygame.mixer.Channel(2).stop()
                
                tempo_fase = (tempo_atual - tempo_inicio_fase_atual) / 1000.0
                tempo_total_corrida += tempo_fase
                
                if fase_atual < 3:
                    fase_atual += 1
                    estado_jogo = "TRANSICAO_FASE"
                    tempo_inicio_transicao = tempo_atual
                    tempo_inicio_fase_atual = tempo_atual
                else:
                    canal_musica.stop()
                    melhores_tempos.append(tempo_total_corrida)
                    melhores_tempos = sorted(melhores_tempos)[:2]
                    salvar_melhores_tempos(melhores_tempos)
                    estado_jogo = "VITORIA"

            tela.blit(recursos_visuais['fundo_img'], (0, 0))
            tela.blit(recursos_visuais['lista_sprites_porta'][3], elementos_fase['pos_entrada'])
            tela.blit(recursos_visuais['lista_sprites_porta'][porta_frame_atual], elementos_fase['pos_saida'])
            elementos_fase['paredes'].draw(tela)
            elementos_fase['todos_sprites'].draw(tela)
            elementos_fase['itens'].draw(tela)
            elementos_fase['obstaculos'].draw(tela)
            desenhar_hud(tela, elementos_fase['hud_vars'], professor, fase_atual, tempo_restante, recursos_visuais['fontes'], recursos_visuais['icones_hud'], estado_som['rect_hud'], estado_som['som_mutado'])

        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == '__main__':
    main()