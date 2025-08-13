import pygame

class Botao:
    def __init__(self, imagem_normal, imagem_hover, pos_x, pos_y):
        """
        Inicializa o botão com duas imagens: uma para o estado normal
        e outra para quando o mouse está sobre ele (hover).
        """
        self.imagem_normal = imagem_normal
        self.imagem_hover = imagem_hover

        self.imagem_atual = self.imagem_normal

        self.rect = self.imagem_atual.get_rect(center=(pos_x, pos_y))

    def desenhar(self, tela):
        """Desenha a imagem atual do botão na tela."""
        tela.blit(self.imagem_atual, self.rect)

    def verificar_input(self, posicao_mouse):
        """Verifica se a posição do mouse está sobre o botão."""
        if self.rect.collidepoint(posicao_mouse):
            return True
        return False

    def atualizar_feedback(self, posicao_mouse):
        """
        Atualiza a imagem do botão (normal ou hover) com base
        na posição do mouse.
        """
        if self.rect.collidepoint(posicao_mouse):
            self.imagem_atual = self.imagem_hover
        else:
            self.imagem_atual = self.imagem_normal