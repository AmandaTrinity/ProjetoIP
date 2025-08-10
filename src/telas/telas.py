import pygame
import sys
from src.utils.desenho import desenhar_texto
from src.utils.constantes import *
from src.movimento.movimento import lidar_movimento_jogador

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

#Executa um ciclo completo do estado 'JOGANDO', incluindo eventos, atualizações e desenho.
#Retorna o próximo estado do jogo e o tempo de início atualizado.
def rodar_estado_jogando(tela, professor, alunos, itens, todos_sprites, paredes, pos_entrada_rect, pos_saida_rect, imagem_fundo, fonte_pequena, tempo_inicio_jogo):    
    # Lógica de Tempo 
    tempo_atual = pygame.time.get_ticks()
    tempo_restante = TEMPO_TOTAL_JOGO - (tempo_atual - tempo_inicio_jogo) // 1000

    # Processamento de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "TELA_INICIAL", tempo_inicio_jogo # Volta para a tela inicial

    direcao_x, direcao_y = lidar_movimento_jogador(professor, paredes)

    # Atualização dos Sprites e Lógica do Jogo
    professor.update(tempo_atual)
    alunos.update(tempo_atual)
    itens.update()
    
    # Verificação de Colisões
    itens_colididos = pygame.sprite.spritecollide(professor, itens, False, pygame.sprite.collide_mask)
    for item in itens_colididos:
        professor.coletar_item(item)

    if not professor.invisivel:
        if pygame.sprite.spritecollide(professor, alunos, False, pygame.sprite.collide_mask):
            tempo_inicio_jogo -= 2000 # Penalidade: perde 2 segundos
            professor.rect.x -= direcao_x * 10
            professor.rect.y -= direcao_y * 10

    # Desenho na Tela 
    if imagem_fundo:
        tela.blit(imagem_fundo, (0,0))
    else:
        tela.fill(CINZA)
    
    pygame.draw.rect(tela, AZUL_CLARO_ENTRADA, pos_entrada_rect)
    pygame.draw.rect(tela, LARANJA, pos_saida_rect)
    
    paredes.draw(tela)
    todos_sprites.draw(tela)
    itens.draw(tela)
    alunos.draw(tela)

    desenhar_texto(f"Tempo: {int(tempo_restante)}", fonte_pequena, BRANCO, tela, 10, 10)
    desenhar_texto(f"Itens: {len(professor.itens_coletados)}/3", fonte_pequena, BRANCO, tela, 10, 40)
    
    if len(professor.itens_coletados) == 3 and professor.rect.colliderect(pos_saida_rect):
        return "VITORIA", tempo_inicio_jogo
    if tempo_restante <= 0:
        return "DERROTA", tempo_inicio_jogo

    return "JOGANDO", tempo_inicio_jogo