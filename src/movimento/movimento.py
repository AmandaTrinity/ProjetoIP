import pygame

#    Verifica as teclas pressionadas e move o professor, aplicando efeitos como o de embriaguez.

def lidar_movimento_jogador(professor, paredes):
    teclas = pygame.key.get_pressed()
    direcao_x, direcao_y = 0, 0

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: direcao_x = -1
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: direcao_x = 1
    if teclas[pygame.K_UP] or teclas[pygame.K_w]: direcao_y = -1
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: direcao_y = 1

    # Efeito da Pitú (bêbado) inverte os controles
    if professor.drunk:
        direcao_x *= -1
        direcao_y *= -1

    professor.mover(direcao_x, direcao_y, paredes)

    return direcao_x, direcao_y