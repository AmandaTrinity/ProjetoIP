# main.py
import pygame
import sys
import os
from src.utils.constantes import *
from src.utils.desenho import desenhar_hud, desenhar_texto
from src.mecanicas.level import setup_fase
from src.utils.audio import SomFalso, toggle_mute
from src.telas.telas import desenhar_tela_inicial, exibir_tela_final, desenhar_tela_confirmacao_reset
from src.utils.pontuacao import carregar_melhores_tempos, salvar_melhores_tempos

def main():
    pygame.init()
    pygame.mixer.init()

    tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # --- CARREGAMENTO DE RECURSOS GLOBAIS ---
    try:
        ss_telhados = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'telhadoscoloridos.png')).convert()
        lista_telhados = [ss_telhados.subsurface((i * 40, 0), (40, 40)) for i in range(6)]
        fundo_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'chãojogo.jpg')).convert(), (LARGURA_TELA, ALTURA_TELA))
        spritesheet_porta = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'porta_entrada_saida.png')).convert_alpha()
        lista_sprites_porta = [spritesheet_porta.subsurface((i * TAMANHO_BLOCO, 0), (TAMANHO_BLOCO, TAMANHO_BLOCO)) for i in range(4)]
        caminho_fonte = os.path.join(DIRETORIO_FONTES, 'PressStart2P-Regular.ttf')
        fontes = {
            'grande': pygame.font.Font(caminho_fonte, 36), 'media': pygame.font.Font(caminho_fonte, 26),
            'pequena': pygame.font.Font(caminho_fonte, 16), 'mini': pygame.font.Font(caminho_fonte, 12),
            'minuscula': pygame.font.Font(caminho_fonte, 8)
        }
        icones_hud = {
            'sombrinha': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'sprite_sheetsombrinha.png')).convert_alpha().subsurface((0,0), (26,26)), (40, 40)),
            'pitu': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'pitu.png')).convert_alpha().subsurface((0,0), (60,190)), (20, 50)),
            'mascara': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'FantasiaVampiro 19x25.png')).convert_alpha().subsurface((0,0), (19,25)), (35, 45))
        }
    except pygame.error as e:
        print(f"Erro fatal ao carregar assets essenciais: {e}")
        pygame.quit()
        sys.exit()

    # Carregamento de sons
    try:
        sons = {
            'inicio': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'musica_inicio.mp3')),
            'jogo': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'musica_jogo.mp3')),
            'andando': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'andando.mp3')),
            'sombrinha': pygame.mixer.Sound(os.path.join(DIRETORIO_SONS, 'som_sombrinha.wav'))
        }
    except pygame.error:
        print("Aviso: Um ou mais sons não puderam ser carregados. Usando sons falsos.")
        sons = {k: SomFalso() for k in ['inicio', 'jogo', 'andando', 'sombrinha']}

    pygame.mixer.set_num_channels(3)
    canal_musica = pygame.mixer.Channel(0)
    
    # --- VARIÁVEIS DE ESTADO DO JOGO ---
    som_mutado = False
    botao_mudo_rect_hud = pygame.Rect(LARGURA_BARRA_LATERAL - 45, 10, 35, 30)
    botao_mudo_rect_menu = pygame.Rect(10, 10, 35, 30)
    
    melhores_tempos = carregar_melhores_tempos()
    tempo_total_corrida = 0.0
    tempo_inicio_fase_atual = 0
    
    estado_jogo = "TELA_INICIAL"
    fase_atual = 1
    tempo_inicio_transicao = 0
    tempo_inicio_jogo = 0
    porta_animando = False
    porta_frame_atual = 0
    porta_ultimo_update = 0
    
    elementos_fase = {}

    # --- LOOP PRINCIPAL ---
    while True:
        tempo_atual = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                rect_clicado_mudo = botao_mudo_rect_menu if estado_jogo != "JOGANDO" else pygame.Rect(LARGURA_TELA + botao_mudo_rect_hud.x, botao_mudo_rect_hud.y, botao_mudo_rect_hud.width, botao_mudo_rect_hud.height)
                if rect_clicado_mudo.collidepoint(evento.pos):
                    som_mutado = toggle_mute(som_mutado)

            if evento.type == pygame.KEYDOWN:
                ### ALTERADO ### - Lógica de teclado agora considera o estado de confirmação
                if estado_jogo == "CONFIRMAR_RESET":
                    if evento.key == pygame.K_RETURN: # Confirma o reset
                        melhores_tempos = [float('inf'), float('inf')]
                        salvar_melhores_tempos(melhores_tempos)
                        estado_jogo = "TELA_INICIAL"
                    elif evento.key == pygame.K_ESCAPE: # Cancela o reset
                        estado_jogo = "TELA_INICIAL"
                
                else: # Lógica de teclado para os outros estados
                    if evento.key == pygame.K_m:
                        som_mutado = toggle_mute(som_mutado)
                    elif evento.key == pygame.K_ESCAPE:
                        canal_musica.stop()
                        pygame.mixer.Channel(2).stop()
                        estado_jogo = "TELA_INICIAL"
                    elif evento.key == pygame.K_r and estado_jogo == "TELA_INICIAL":
                        estado_jogo = "CONFIRMAR_RESET" # Apenas muda para o estado de confirmação
                    elif evento.key == pygame.K_RETURN:
                        if estado_jogo == "TELA_INICIAL":
                            fase_atual = 1
                            elementos_fase = setup_fase(fase_atual, lista_telhados, sons)
                            tempo_inicio_jogo = tempo_atual
                            tempo_total_corrida = 0.0
                            tempo_inicio_fase_atual = tempo_atual
                            porta_animando, porta_frame_atual = False, 0
                            canal_musica.stop()
                            canal_musica.play(sons['jogo'], -1)
                            estado_jogo = "JOGANDO"
                        elif estado_jogo in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"]:
                            estado_jogo = "TELA_INICIAL"
        
        # --- LÓGICA DE ESTADOS ---
        if estado_jogo == "TELA_INICIAL":
            if not canal_musica.get_busy():
                canal_musica.play(sons['inicio'], -1)
            desenhar_tela_inicial(tela, fontes, melhores_tempos, som_mutado, botao_mudo_rect_menu)

        ### NOVO ### - Estado para desenhar o pop-up de confirmação
        elif estado_jogo == "CONFIRMAR_RESET":
            # Primeiro, desenha a tela inicial por baixo para criar o efeito de pop-up
            desenhar_tela_inicial(tela, fontes, melhores_tempos, som_mutado, botao_mudo_rect_menu)
            desenhar_tela_confirmacao_reset(tela, fontes)

        elif estado_jogo == "TRANSICAO_FASE":
            tela.fill(PRETO)
            desenhar_texto(f"FASE {fase_atual}", fontes['grande'], BRANCO, tela, LARGURA_TOTAL / 2, ALTURA_TELA / 2, True)
            if tempo_atual - tempo_inicio_transicao > 3000:
                elementos_fase = setup_fase(fase_atual, lista_telhados, sons)
                tempo_inicio_jogo = tempo_atual
                porta_animando, porta_frame_atual = False, 0
                estado_jogo = "JOGANDO"

        elif estado_jogo in ["VITORIA", "DERROTA", "DERROTA_OBSTACULO"]:
            mensagens_fim = {
                "VITORIA": (VERDE, "VOCÊ CONSEGUIU!", "RUMO AO CARNAVAL!"),
                "DERROTA": (VERMELHO, "TEMPO ESGOTADO!", "Mais um ano no CIn..."),
                "DERROTA_OBSTACULO": (VERMELHO, "GAME OVER!", "Você não sobreviveu à multidão.")
            }
            cor, msg1, msg2 = mensagens_fim[estado_jogo]
            tempo_a_exibir = tempo_total_corrida if estado_jogo == "VITORIA" else None
            exibir_tela_final(tela, cor, msg1, msg2, fontes, botao_mudo_rect_menu, som_mutado, tempo_partida=tempo_a_exibir)

        elif estado_jogo == "JOGANDO":
            professor = elementos_fase['professor']
            teclas = pygame.key.get_pressed()
            dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
            dy = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])
            if professor.drunk: dx, dy = -dx, -dy
            
            movimento_real = professor.mover(dx, dy, elementos_fase['paredes'])
            professor.update(tempo_atual, movimento_real)
            elementos_fase['obstaculos'].update(tempo_atual)
            elementos_fase['itens'].update()

            for item in pygame.sprite.spritecollide(professor, elementos_fase['itens'], False, pygame.sprite.collide_mask):
                professor.coletar_item(item, elementos_fase['hud_vars'])
            
            if not professor.invisivel and pygame.sprite.spritecollide(professor, elementos_fase['obstaculos'], False, pygame.sprite.collide_mask):
                if fase_atual == 3:
                    canal_musica.stop(); pygame.mixer.Channel(2).stop(); estado_jogo = "DERROTA_OBSTACULO"
                else:
                    tempo_inicio_jogo -= 2000
                    professor.hitbox.x -= dx * professor.velocidade * 4
                    professor.hitbox.y -= dy * professor.velocidade * 4
            
            if len(professor.itens_coletados) == 3 and not porta_animando and porta_frame_atual == 0:
                porta_animando = True
                porta_ultimo_update = tempo_atual
            
            if porta_animando and tempo_atual - porta_ultimo_update > 200:
                porta_ultimo_update = tempo_atual
                porta_frame_atual = min(porta_frame_atual + 1, len(lista_sprites_porta) - 1)
                if porta_frame_atual == len(lista_sprites_porta) - 1:
                    porta_animando = False
            
            tempo_restante = TEMPO_TOTAL_JOGO - (tempo_atual - tempo_inicio_jogo) / 1000
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

            tela.blit(fundo_img, (0, 0))
            tela.blit(lista_sprites_porta[3], elementos_fase['pos_entrada'])
            tela.blit(lista_sprites_porta[porta_frame_atual], elementos_fase['pos_saida'])
            elementos_fase['paredes'].draw(tela)
            elementos_fase['todos_sprites'].draw(tela)
            elementos_fase['itens'].draw(tela)
            elementos_fase['obstaculos'].draw(tela)
            desenhar_hud(tela, elementos_fase['hud_vars'], professor, fase_atual, tempo_restante, fontes, icones_hud, botao_mudo_rect_hud, som_mutado)

        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == '__main__':
    main()