import pygame
import sys
import os
from src.utils.constantes import *
from src.utils.audio import *
from src.utils.setup import iniciar_jogo, carregar_recursos, carregar_fontes
from src.telas.telas import tela_inicial, tela_vitoria, tela_derrota, lidar_eventos_fim_de_jogo, rodar_estado_jogando

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Jogo Principal
def main():
    # Inicialização do Pygame e Recursos
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    lista_telhados, imagem_fundo = carregar_recursos()

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
            estado_jogo, tempo_inicio_jogo = rodar_estado_jogando(
                tela, professor, alunos, itens, todos_sprites, paredes,
                pos_entrada_rect, pos_saida_rect, imagem_fundo,
                fonte_pequena, tempo_inicio_jogo)

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