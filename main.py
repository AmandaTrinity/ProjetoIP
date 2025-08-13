# main.py
import pygame
from src.utils.constantes import *
from src.utils.desenho import desenhar_hud, desenhar_texto
from src.mecanicas.level import setup_fase
from src.utils.audio import carregar_sons
from src.telas.telas import desenhar_tela_inicial, exibir_tela_final, desenhar_menu_popup
from src.utils.pontuacao import carregar_melhores_tempos, salvar_melhores_tempos
from src.utils.setup import carregar_recursos_globais
from src.utils.botao import Botao 
from src.mecanicas.eventos import processar_eventos

def main():
    pygame.init()
    pygame.mixer.init()

    tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # CARREGAMENTO DE RECURSOS GLOBAIS
    recursos_visuais = carregar_recursos_globais()
    sons = carregar_sons()

    botao_iniciar = Botao(
        imagem_normal=recursos_visuais['imagens_botao_inicial']['normal'],
        imagem_hover=recursos_visuais['imagens_botao_inicial']['clicado'], # Usamos a imagem de 'clicado' para o hover
        pos_x=LARGURA_TOTAL / 2, 
        pos_y=ALTURA_TELA / 2 + 40
    )
    
    botao_menu = Botao(
        imagem_normal=recursos_visuais['imagens_botao_menu']['normal'], # Pode usar a mesma imagem por enquanto
        imagem_hover=recursos_visuais['imagens_botao_menu']['clicado'],
        pos_x=LARGURA_TOTAL / 2,
        pos_y=ALTURA_TELA / 2 + 120
    ) 

    botao_reiniciar = Botao(
        imagem_normal=recursos_visuais['imagens_botao_reiniciar']['normal'], # Usando a arte do botão de menu como exemplo
        imagem_hover=recursos_visuais['imagens_botao_reiniciar']['clicado'],
        pos_x=LARGURA_TOTAL / 2,
        pos_y=(ALTURA_TELA * 5 / 6) - 50
    )

    pygame.mixer.set_num_channels(3)
    canal_musica = pygame.mixer.Channel(0)
    
    # VARIÁVEIS DE ESTADO DO JOGO
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

    # LOOP PRINCIPAL
    while True:

        tempo_atual = pygame.time.get_ticks()

        botoes_para_passar = None

        if estado_jogo == "TELA_INICIAL":
            botoes_para_passar = {'iniciar': botao_iniciar, 'menu': botao_menu}

        elif estado_jogo == "TELA_MENU":
            botoes_para_passar = None
        
        elif estado_jogo in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"]:
            botoes_para_passar = {'reiniciar': botao_reiniciar}

        comandos_usuario = processar_eventos(estado_jogo, estado_som, botoes_para_passar)
        estado_som['som_mutado'] = comandos_usuario['som_mutado']

        # ATUALIZAÇÃO DE ESTADO BASEADO NOS COMANDOS ---
        acao = comandos_usuario.get('acao')
        if acao == 'VOLTAR_MENU':
            canal_musica.stop(); pygame.mixer.Channel(2).stop()
            estado_jogo = "TELA_INICIAL"

        elif acao == 'ABRIR_MENU':
            estado_jogo = "TELA_MENU"

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

        elif acao == 'RESETAR_PONTUACAO':
            melhores_tempos = [float('inf'), float('inf')]
            salvar_melhores_tempos(melhores_tempos)
            estado_jogo = "TELA_INICIAL"
        
        # LÓGICA DE ESTADOS
        if estado_jogo == "TELA_INICIAL":
            if not canal_musica.get_busy():
                canal_musica.play(sons['inicio'], -1)
            desenhar_tela_inicial(tela, recursos_visuais, estado_som['som_mutado'], estado_som['rect_menu'], botao_iniciar, botao_menu)

        elif estado_jogo == "TELA_MENU":
            tela.blit(recursos_visuais['fundo_tela_inicial'], (0, 0))
            desenhar_menu_popup(tela, recursos_visuais, melhores_tempos)

        elif estado_jogo == "TRANSICAO_FASE":
            if fase_atual == 2:
                tela.blit(recursos_visuais['fundo_transicao_1_2'], (0, 0))
            if fase_atual == 3:
                tela.blit(recursos_visuais['fundo_transicao_2_3'], (0, 0))

            if tempo_atual - tempo_inicio_transicao > 3000:
                elementos_fase = setup_fase(fase_atual, recursos_visuais['lista_telhados'], sons)
                ponto_referencia_timer_regressivo = tempo_atual
                porta_animando, porta_frame_atual = False, 0
                estado_jogo = "JOGANDO"
                
        if estado_jogo == "VITORIA":
            tela.blit(recursos_visuais['fundo_vitoria'], (0, 0))
            posicao_mouse = pygame.mouse.get_pos()
            botao_reiniciar.atualizar_feedback(posicao_mouse)
            botao_reiniciar.desenhar(tela)

        elif estado_jogo == "DERROTA": # Quando o tempo acaba
            # APENAS desenha a sua nova imagem de derrota por tempo
            tela.blit(recursos_visuais['fundo_derrota_tempo'], (0, 0))
            # E o texto para voltar
            posicao_mouse = pygame.mouse.get_pos()
            botao_reiniciar.atualizar_feedback(posicao_mouse)
            botao_reiniciar.desenhar(tela)
        elif estado_jogo == "DERROTA_OBSTACULO": # Quando colide com a La Ursa
            # APENAS desenha a sua nova imagem de derrota pela La Ursa
            tela.blit(recursos_visuais['fundo_derrota_laursa'], (0, 0))
            # E o texto para voltar
            posicao_mouse = pygame.mouse.get_pos()
            botao_reiniciar.atualizar_feedback(posicao_mouse)
            botao_reiniciar.desenhar(tela)       

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
            
            laursas_colididas = pygame.sprite.spritecollide(professor, elementos_fase['obstaculos'], False, pygame.sprite.collide_mask)
            if not professor.invisivel and laursas_colididas:
                laursa_atingida = laursas_colididas[0]
                if fase_atual == 3:
                    canal_musica.stop(); pygame.mixer.Channel(2).stop(); estado_jogo = "DERROTA_OBSTACULO"
                else:
                    ponto_referencia_timer_regressivo -= laursa_atingida.penalidade_tempo_ms
                    professor.hitbox.center = elementos_fase['pos_entrada'].center
            
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
                    canal_musica.unpause()
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