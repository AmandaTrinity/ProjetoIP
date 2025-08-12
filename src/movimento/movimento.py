# src/movimento/movimento.py
import pygame

def mover_personagem(personagem, desloc_x, desloc_y, paredes):
    """
    Move um personagem com detecção de colisão por eixo.
    Atualiza a direção do personagem e retorna True se houve movimento.
    """
    # Primeiro, movemos e verificamos a colisão no eixo X (horizontal)
    personagem.hitbox.x += desloc_x * personagem.velocidade
    personagem.rect.centerx = personagem.hitbox.centerx

    colisoes_x = pygame.sprite.spritecollide(personagem, paredes, False, pygame.sprite.collide_mask)
    if colisoes_x:
        # Se colidiu, voltamos à posição X anterior ao movimento
        personagem.hitbox.x -= desloc_x * personagem.velocidade
        personagem.rect.centerx = personagem.hitbox.centerx

    # Agora, fazemos o mesmo para o eixo Y (vertical)
    personagem.hitbox.y += desloc_y * personagem.velocidade
    personagem.rect.centery = personagem.hitbox.centery

    colisoes_y = pygame.sprite.spritecollide(personagem, paredes, False, pygame.sprite.collide_mask)
    if colisoes_y:
        # Se colidiu, voltamos à posição Y anterior ao movimento
        personagem.hitbox.y -= desloc_y * personagem.velocidade
        personagem.rect.centery = personagem.hitbox.centery

    # Atualiza a direção do sprite com base na intenção de movimento horizontal
    if desloc_x > 0:
        personagem.direcao = 'direita'
    elif desloc_x < 0:
        personagem.direcao = 'esquerda'

    # Retorna se o personagem teve alguma intenção de movimento
    personagem_se_moveu = (desloc_x != 0 or desloc_y != 0)
    return personagem_se_moveu