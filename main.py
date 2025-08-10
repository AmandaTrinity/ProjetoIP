import pygame
import sys
import os
from src.utils.constantes import *
from src.utils.audio import *
from src.utils.desenho import desenhar_texto
from src.utils.setup import iniciar_jogo, carregar_fontes
from src.telas.telas import tela_inicial, tela_vitoria, tela_derrota, lidar_eventos_fim_de_jogo
from src.movimento.movimento import lidar_movimento_jogador

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Jogo Principal
def main():
    # Inicialização do Pygame e Recursos
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # Carrega a sprite sheet dos telhados e cria uma lista de imagens individuais
    ss_telhados = pygame.image.load(os.path.join(SPRITES_DIR, 'telhadoscoloridos.png')).convert()
    lista_telhados = []
    for i in range(8): # O número de telhados de cores diferentes na sprite sheet
        img_t = ss_telhados.subsurface((i * 40, 0), (40, 40))
        lista_telhados.append(img_t)

    # Carrega a imagem de fundo do jogo
    try:
        caminho_fundo = os.path.join(SPRITES_DIR, 'chãojogo.jpg')
        fundo_img=pygame.image.load(caminho_fundo).convert()
        fundo_img = pygame.transform.scale(fundo_img, (LARGURA_TELA, ALTURA_TELA))
        print("Imagem de fundo carreagado com sucesso!")
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        fundo_img = None # Se a imagem falhar, usaremos uma cor de fundo sólida
    
    fonte_grande,fonte_media,fonte_pequena = carregar_fontes()
    
    # Variáveis de Estado do Jogo 
    estado_jogo = "TELA_INICIAL"
    
    # Loop Principal do Jogo
    while True:
        # Estado: TELA INICIAL
        if estado_jogo == "TELA_INICIAL":
            tela_inicial(tela,fonte_grande,fonte_media,fonte_pequena,som_inicio)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        # Muda o estado para 'JOGANDO'
                        estado_jogo = "JOGANDO"
                        
                        # Para a música da tela inicial e inicia a música do jogo
                        som_inicio.stop()
                        som_jogo.play(-1)
                                                
                        # Configura e inicializa os elementos da fase
                        paredes, pos_entrada_rect, pos_saida_rect, professor, itens, todos_sprites, alunos, tempo_inicio_jogo = iniciar_jogo(lista_telhados)

                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        # Estado: JOGANDO
        elif estado_jogo == "JOGANDO":
            # Lógica de Tempo 
            tempo_atual = pygame.time.get_ticks()
            tempo_restante = TEMPO_TOTAL_JOGO - (tempo_atual - tempo_inicio_jogo) // 1000

            # Processamento de Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    estado_jogo = "TELA_INICIAL" # Volta para a tela inicial

            dx, dy = lidar_movimento_jogador(professor, paredes)

            # Atualização dos Sprites e Lógica do Jogo
            professor.update(tempo_atual)
            alunos.update(tempo_atual)
            itens.update()
            
            # Verificação de Colisões
            itens_colididos = pygame.sprite.spritecollide(professor, itens, False, pygame.sprite.collide_mask)
            for item in itens_colididos:
                professor.coletar_item(item)

            # Colisão com alunos
            if not professor.invisivel:
                if pygame.sprite.spritecollide(professor, alunos, False, pygame.sprite.collide_mask):
                    tempo_inicio_jogo -= 2000 # Penalidade: perde 2 segundos
                    # Empurra o professor para uma posição segura
                    professor.rect.x -= dx * 10
                    professor.rect.y -= dy * 10

            # Desenho na Tela 
            if fundo_img: # Se a imagem de fundo foi carregada, a desenha
                tela.blit(fundo_img, (0,0))
            else:
                tela.fill(CINZA) # Caso contrário, preenche com uma cor sólida
            
            # Desenha os elementos do labirinto e os sprites
            pygame.draw.rect(tela, AZUL_CLARO_ENTRADA, pos_entrada_rect)
            pygame.draw.rect(tela, LARANJA, pos_saida_rect)
            
            paredes.draw(tela)
            todos_sprites.draw(tela)
            itens.draw(tela)
            alunos.draw(tela)

            # Desenhar HUD (Heads-Up Display)
            desenhar_texto(f"Tempo: {int(tempo_restante)}", fonte_pequena, BRANCO, tela, 10, 10)
            desenhar_texto(f"Itens: {len(professor.itens_coletados)}/3", fonte_pequena, BRANCO, tela, 10, 40)
            
            # Verificação de Condição de Vitória/Derrota
            if len(professor.itens_coletados) == 3 and professor.rect.colliderect(pos_saida_rect):
                estado_jogo = "VITORIA"
            
            if tempo_restante <= 0:
                estado_jogo = "DERROTA"

        # Estado: VITÓRIA
        elif estado_jogo == "VITORIA":
            tela_vitoria(tela,fonte_grande,fonte_media,fonte_pequena)
            estado_jogo = lidar_eventos_fim_de_jogo(estado_jogo)

        # Estado: DERROTA
        elif estado_jogo == "DERROTA":
            tela_derrota(tela,fonte_grande,fonte_media,fonte_pequena)
            estado_jogo = lidar_eventos_fim_de_jogo(estado_jogo)

        # Atualização da Tela
        # Desenha tudo o que foi preparado na tela
        pygame.display.flip()
        # Garante que o jogo rode na velocidade definida por FPS
        relogio.tick(FPS)

# Garante que o jogo só rode quando o script é executado diretamente
if __name__ == '__main__':
    main()