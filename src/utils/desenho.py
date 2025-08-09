def desenhar_texto(texto, fonte, cor, superficie, x, y, centro=False):
    """Função para desenhar texto na tela."""
    objeto_texto = fonte.render(texto, True, cor)
    rect_texto = objeto_texto.get_rect()
    if centro:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    superficie.blit(objeto_texto, rect_texto)