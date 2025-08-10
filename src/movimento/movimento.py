import pygame

#    Verifica as teclas pressionadas e move o professor, aplicando efeitos como o de embriaguez.

def lidar_movimento_jogador(professor, paredes):
    teclas = pygame.key.get_pressed()
    dx, dy = 0, 0

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: dx = -1
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dx = 1
    if teclas[pygame.K_UP] or teclas[pygame.K_w]: dy = -1
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: dy = 1

    # Efeito da Pitú (bêbado) inverte os controles
    if professor.drunk:
        dx *= -1
        dy *= -1

    professor.mover(dx, dy, paredes)

    return dx,dy