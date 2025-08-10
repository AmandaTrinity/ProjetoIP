import pygame
import sys
import random
import os
from src.utils.constantes import *
from src.utils.audio import *
from src.utils.desenho import desenhar_texto
from src.personagens.professor import Professor
from src.personagens.aluno import Aluno
from src.coletaveis.sombrinha import SombrinhaFrevo
from src.coletaveis.garrafaPitu import GarrafaPitu
from src.coletaveis.fantasiaCarnaval import FantasiaCarnaval
from src.labirinto.labirinto import criar_labirinto
from src.telas.telas import tela_inicial, tela_vitoria, tela_derrota

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- Jogo Principal ---
def main():
    """Função principal que roda o jogo."""
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # criação da lista das sprite_sheets dos telhados
    ss_telhados = pygame.image.load(os.path.join(SPRITES_DIR, 'telhadoscoloridos.png')).convert()
    lista_telhados = []
    for i in range(8): # número de telhados de cores diferentes
        img_t = ss_telhados.subsurface((i * 40, 0), (40, 40))
        lista_telhados.append(img_t)
    # carregar imagem do chão
    try:
        caminho_fundo = os.path.join(SPRITES_DIR, 'chãojogo.jpg')
        fundo_img=pygame.image.load(caminho_fundo).convert()

        fundo_img = pygame.transform.scale(fundo_img, (LARGURA_TELA, ALTURA_TELA))
        print("Imagem de fundo carreagado com sucesso!")
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        fundo_img = None #Usaremos uma cor

    # Fontes
    fonte_grande = pygame.font.Font(None, 74)
    fonte_media = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 36)
    
    # Variáveis de estado do jogo
    estado_jogo = "TELA_INICIAL"
    
    # Loop principal
    while True:
        if estado_jogo == "TELA_INICIAL":
            tela_inicial(tela,fonte_grande,fonte_media,fonte_pequena,som_inicio)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        estado_jogo = "JOGANDO"
                        # Transiciona as músicas
                        som_inicio.stop()
                        som_jogo.play(-1)
                        # Reinicia as variáveis do jogo
                        paredes, pos_validas, pos_e_centro, pos_e_rect, pos_s_rect = criar_labirinto(lista_telhados)
                        pos_entrada_rect = pos_e_rect
                        pos_saida_rect = pos_s_rect
                        
                        professor = Professor(*pos_e_centro)
                        
                        # Posiciona itens aleatoriamente
                        if len(pos_validas) >= 3:
                            pos_itens = random.sample(pos_validas, 3)
                        else:
                            print("AVISO: Não há posições válidas suficientes para todos os itens!")
                            pos_itens = pos_validas # Coloca itens onde for possível
                        
                        itens = pygame.sprite.Group()
                        if len(pos_itens) > 0: itens.add(SombrinhaFrevo(pos_itens[0]))
                        if len(pos_itens) > 1: itens.add(GarrafaPitu(pos_itens[1]))
                        if len(pos_itens) > 2: itens.add(FantasiaCarnaval(pos_itens[2]))
                        
                        todos_sprites = pygame.sprite.Group(professor)
                        
                        # Adiciona alunos
                        alunos = pygame.sprite.Group()
                        alunos.add(Aluno(5 * TAMANHO_BLOCO, 7 * TAMANHO_BLOCO))
                        alunos.add(Aluno(13 * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO))

                        tempo_inicio_jogo = pygame.time.get_ticks()
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        elif estado_jogo == "JOGANDO":
            tempo_atual = pygame.time.get_ticks()
            tempo_restante = TEMPO_TOTAL_JOGO - (tempo_atual - tempo_inicio_jogo) // 1000

            # --- Lógica de Eventos ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    estado_jogo = "TELA_INICIAL" # Volta para a tela inicial

            # --- Lógica de Movimento ---
            teclas = pygame.key.get_pressed()
            dx, dy = 0, 0
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: dx = -1
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dx = 1
            if teclas[pygame.K_UP] or teclas[pygame.K_w]: dy = -1
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: dy = 1
            
            # Efeito da Pitú inverte os controles
            if professor.drunk:
                dx *= -1
                dy *= -1

            professor.mover(dx, dy, paredes)

            # --- Lógica de Atualização ---
            professor.update(tempo_atual)
            alunos.update(tempo_atual)
            itens.update()
            
            # Colisão com itens
            itens_colididos = pygame.sprite.spritecollide(professor, itens, False, pygame.sprite.collide_mask) #Alteração aqui para colidir por pixel
            for item in itens_colididos:
                professor.coletar_item(item)

            # Colisão com alunos
            if not professor.invisivel:
                if pygame.sprite.spritecollide(professor, alunos, False, pygame.sprite.collide_mask):
                    tempo_inicio_jogo -= 2000 # Penalidade: perde 2 segundos
                    # Empurra o professor para uma posição segura
                    professor.rect.x -= dx * 10
                    professor.rect.y -= dy * 10

            # --- Lógica de Desenho ---
            if fundo_img: #ou seja, a imagem foi carregada com sucesso
                tela.blit(fundo_img, (0,0))
            else:
                tela.fill(CINZA) #Alterado para cinza para melhor visualização do personagemz
            
            # Desenha entrada e saída
            pygame.draw.rect(tela, AZUL_CLARO_ENTRADA, pos_entrada_rect)
            pygame.draw.rect(tela, LARANJA, pos_saida_rect)
            
            paredes.draw(tela)
            todos_sprites.draw(tela)
            itens.draw(tela)
            alunos.draw(tela)

            # Desenhar HUD (Heads-Up Display)
            desenhar_texto(f"Tempo: {int(tempo_restante)}", fonte_pequena, BRANCO, tela, 10, 10)
            desenhar_texto(f"Itens: {len(professor.itens_coletados)}/3", fonte_pequena, BRANCO, tela, 10, 40)
            
            # --- Lógica de Vitória/Derrota ---
            if len(professor.itens_coletados) == 3 and professor.rect.colliderect(pos_saida_rect):
                estado_jogo = "VITORIA"
            
            if tempo_restante <= 0:
                estado_jogo = "DERROTA"

        elif estado_jogo == "VITORIA":
            tela_vitoria(tela,fonte_grande,fonte_media,fonte_pequena)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado_jogo = "TELA_INICIAL"

        elif estado_jogo == "DERROTA":
            tela_derrota(tela,fonte_grande,fonte_media,fonte_pequena)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado_jogo = "TELA_INICIAL"

        # Atualiza a tela inteira
        pygame.display.flip()
        # Controla a taxa de quadros por segundo (FPS)
        relogio.tick(FPS)

if __name__ == '__main__':
    main()