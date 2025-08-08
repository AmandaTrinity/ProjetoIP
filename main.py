# -*- coding: utf-8 -*-
import pygame
import sys
import random
import os

# --- Configurações e Constantes ---
# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL_CIN = (50, 100, 150)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
CIANO = (0, 255, 255)
AZUL_CLARO_ENTRADA = (173, 216, 230) # Cor para a entrada

# Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_BLOCO = 40

# Jogo
TITULO_JOGO = "Jornada para o Carnaval"
FPS = 30
TEMPO_TOTAL_JOGO = 60  # em segundos

# --- Estrutura do Labirinto ---
# 'P' = Parede, 'C' = Corredor, 'E' = Entrada, 'S' = Saída
LAYOUT_LABIRINTO = [
    "PPPPPPPPPPPPPPPPPPPP",
    "PECCCCCCCCPCCCCCCSPP",
    "PCPPPPPCCPCPPCPPPCPP",
    "PCCCPCCCCCPCPCCCCCCP",
    "PPCPPPCPPPCPPPCPPPCP",
    "PCPCCCCCPCCCCCPCCCCP",
    "PCPPPCPCPPPCPCPPPCPP",
    "PCCCCPCCCCPCPCCCCCCP",
    "PCPPPCPPPCPCPPPCPCPP",
    "PCPCCCCCPCCCCCPCCCCP",
    "PCPPPCPCPPPCPCPPPCPP",
    "PCCCPCCCCCPCCCCCCPCP",
    "PPPPPCPPPCPPPCPCPCPP",
    "PCCCCCPCCCCCPCCCCCCP",
    "PPPPPPPPPPPPPPPPPPPP",
]

# Diretórios 
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

# --- Classes do Jogo ---

class Professor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- Lógica de Animação ---
        diretorio_atual = os.path.dirname(__file__)
        caminho_para_imagens = os.path.join(diretorio_atual, 'Imagens')

        self.animacoes = {}
        self.parado = {}
        try:
            frames_normais_direita = [] #Adiciona imagens andando para direita
            for i in range(4):
                nome_do_arquivo = f"stefan_direita{i}.png"
                caminho_completo = os.path.join(caminho_para_imagens, nome_do_arquivo)
                
                print(f"Tentando carregar: {caminho_completo}") 
                
                frame_direita = pygame.image.load(caminho_completo).convert_alpha()
                frame_direita = pygame.transform.scale(frame_direita, (40, 40))
                frames_normais_direita.append(frame_direita)

            self.animacoes['normal direita'] = frames_normais_direita
            frames_normais_esquerda = []
            for i in range(4): #Adiciona imagens andando para esquerda
                nome_do_arquivo = f"stefan_esquerda{i}.png"
                caminho_completo = os.path.join(caminho_para_imagens, nome_do_arquivo)
                
                print(f"Tentando carregar: {caminho_completo}") 
                
                frame_esquerda = pygame.image.load(caminho_completo).convert_alpha()
                frame_esquerda = pygame.transform.scale(frame_esquerda, (40, 40))
                frames_normais_esquerda.append(frame_esquerda)

            self.animacoes['normal esquerda'] = frames_normais_esquerda
            self.parado = {'normal direita': self.animacoes['normal direita'][0], 'normal esquerda': self.animacoes['normal esquerda'][0]}
            
            #Carregar imagens fantasiados
            vampiro_direita_lista=[]
            for i in range(4):
                nome_do_arquivo = f"stefanvampiro_direita{i}.png"
                caminho_completo = os.path.join(caminho_para_imagens, nome_do_arquivo)
                
                print(f"Tentando carregar: {caminho_completo}") 
                
                vampiro_direita = pygame.image.load(caminho_completo).convert_alpha()
                vampiro_direita = pygame.transform.scale(vampiro_direita, (40, 40))
                vampiro_direita_lista.append(vampiro_direita)
            self.animacoes['vampiro direita'] = vampiro_direita_lista

            vampiro_esquerda_lista=[]
            for i in range(4):
                nome_do_arquivo = f"stefanvampiroesqueda_{i}.png"
                caminho_completo = os.path.join(caminho_para_imagens, nome_do_arquivo)
                
                print(f"Tentando carregar: {caminho_completo}") 
                
                vampiro_esquerda = pygame.image.load(caminho_completo).convert_alpha()
                vampiro_esquerda = pygame.transform.scale(vampiro_esquerda, (40, 40))
                vampiro_esquerda_lista.append(vampiro_esquerda)

            self.animacoes['vampiro esquerda'] = vampiro_esquerda_lista
            self.parado['vampiro direita'] = self.animacoes['vampiro direita'][0]
            self.parado['vampiro esquerda'] = self.animacoes['vampiro esquerda'][0]

            
        except pygame.error:
            # Caso as imagens não sejam encontradas
            print(f"Erro ao carregar imagens: {i}")
            print("Usando um quadrado amarelo como fallback.")
            
            fallback_surface = pygame.Surface((TAMANHO_BLOCO, int(TAMANHO_BLOCO * 1.5))) #Cria-se uma imagem fallback
            fallback_surface.fill(AMARELO)
            
            # Coloca essa imagem dentro da mesma estrutura de dicionário e lista
            self.animacoes['normal esquerda'] = [fallback_surface] # Uma lista com um único frame
            self.animacoes['normal direita'] = [fallback_surface]
            self.parado['normal esquerda'] = [fallback_surface]
            self.parado['normal direita'] = [fallback_surface]

        self.tipo = 'normal ' #pra definir se é fantasiado ou não, começa normal
        self.direcao='direita' #Inicia olhando para direita
        self.image = self.parado[self.tipo + self.direcao]
        self.frame_atual = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image) #Para aplicar a lógica de colisões pixel com pixel

        # Atributos de controle da animação
        self.animar_agora = False
        self.tempo_animacao = 0
        self.velocidade_animacao = 100 # ms entre frames

        # Atributos do Jogo
        self.velocidade_base = 5
        self.velocidade = self.velocidade_base
        self.itens_coletados = []
        self.invisivel = False
        self.tempo_boost = 0
        self.tempo_invisivel = 0
        self.drunk = False
        self.tempo_drunk = 0


    def mover(self, dx, dy, paredes):
        # O método mover SÓ se preocupa com o movimento.
        # Se o personagem se moveu (dx ou dy não são zero), ativamos a animação.
        if dx != 0 or dy != 0:
            self.animar_agora = True
        else:
            self.animar_agora = False

        #Lógica de direção
        if dx>0:
            self.direcao='direita'
        elif dx<0:
            self.direcao='esquerda'

        self.rect.x += dx * self.velocidade
        for parede in paredes:
            if pygame.sprite.collide_mask(self, parede):
                if dx > 0: self.rect.right = parede.rect.left
                if dx < 0: self.rect.left = parede.rect.right
        
        self.rect.y += dy * self.velocidade
        for parede in paredes:
            if pygame.sprite.collide_mask(self, parede):
                if dy > 0: self.rect.bottom = parede.rect.top
                if dy < 0: self.rect.top = parede.rect.bottom

    def update(self, tempo_atual):
        estado_animacao_atual=self.tipo + self.direcao
        if self.animar_agora:
            # Verifica se já passou tempo suficiente para trocar o frame
            if tempo_atual - self.tempo_animacao > self.velocidade_animacao:
                self.tempo_animacao = tempo_atual # Reseta o contador
                
                #Adicionado para animar para esquerda e para direita
                lista_de_frames_atual=self.animacoes[estado_animacao_atual]
                self.frame_atual = (self.frame_atual + 1) % len(lista_de_frames_atual)
                
                self.image = lista_de_frames_atual[self.frame_atual]
                self.mask = pygame.mask.from_surface(self.image)
        else:
            #Foi definida um novo atributo para quando estiver parado, então se não estivera animando agora, está parado.
            self.image = self.parado[estado_animacao_atual]
            self.image = self.parado[estado_animacao_atual]
            self.frame_atual = 0 #Reseta para o primeiro frame

        if self.tempo_boost > 0 and tempo_atual > self.tempo_boost:
            self.velocidade = self.velocidade_base
            self.tempo_boost = 0
            print("Efeito da Sombrinha acabou!")

        # Efeito da Máscara (invisibilidade)
        if self.tempo_invisivel > 0 and tempo_atual > self.tempo_invisivel:
            self.invisivel = False
            self.tempo_invisivel = 0
            print("Efeito da Máscara acabou!")
            self.image.set_alpha(255) # Volta a ser visível
            
        # Efeito da Garrafa de Pitú (controles trocados)
        if self.tempo_drunk > 0 and tempo_atual > self.tempo_drunk:
            self.drunk = False
            self.tempo_drunk = 0
            print("Efeito da Pitú acabou! Você não está mais tonto.")

    def coletar_item(self, item):
        """Adiciona item à lista e aplica seu efeito."""
        if item.nome not in self.itens_coletados:
            self.itens_coletados.append(item.nome)
            item.aplicar_efeito(self)
            item.kill() # Remove o sprite do item do jogo

class Aluno(pygame.sprite.Sprite):
    """Classe para os obstáculos que se movem."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANHO_BLOCO - 10, TAMANHO_BLOCO - 10))
        self.image.fill(CIANO)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image) #Também precisa colocar máscara nos obstáculos e afins
        self.direcao = 1
        self.movimento_range = 120 # O quanto ele se move para frente e para trás
        self.pos_inicial_y = y

    def update(self):
        """Move o aluno verticalmente."""
        self.rect.y += self.direcao * 2
        if self.rect.y > self.pos_inicial_y + self.movimento_range or self.rect.y < self.pos_inicial_y:
            self.direcao *= -1

class Item(pygame.sprite.Sprite):
    """Classe base para todos os itens coletáveis."""
    def __init__(self, nome, pos, imagens, n_sprites, largura, altura, nova_largura=None, nova_altura=None):
        super().__init__()
        self.nome = nome
        self.image = pygame.Surface((TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2))
        self.rect = self.image.get_rect(center=pos)
        sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, imagens)).convert_alpha()
        self.lista_sprites = []
        for i in range(n_sprites): # número de sprites
            sprite = sprite_sheet.subsurface((i * largura, 0), (largura, altura))
            if nova_altura != None and nova_largura != None:
                sprite = pygame.transform.scale(sprite, (nova_largura, nova_altura))
            self.lista_sprites.append(sprite)

        self.index_lista = 0

        # substituindo imagem placeholder
        self.image = self.lista_sprites[self.index_lista]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.index_lista += 0.15
        if self.index_lista >= len(self.lista_sprites):
            self.index_lista = 0
        self.image = self.lista_sprites[int(self.index_lista)]
        self.mask = pygame.mask.from_surface(self.image)

    def aplicar_efeito(self, professor):
        """Método a ser sobrescrito por cada item."""
        print(f"Item {self.nome} coletado!")

class SombrinhaFrevo(Item):
    def __init__(self, pos):
        super().__init__("Sombrinha de Frevo", pos, 'sprite_sheetsombrinha.png', 3, 26, 26)
        
    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        professor.velocidade = professor.velocidade_base * 2
        professor.tempo_boost = pygame.time.get_ticks() + 5000 # 5 segundos de boost

class GarrafaPitu(Item):
    def __init__(self, pos):
        super().__init__("Garrafa de Pitú", pos, 'pitu.png', 2, 60, 190, 10, 32)

    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        professor.drunk = True
        professor.tempo_drunk = pygame.time.get_ticks() + 7000 # 7 segundos de tontura

class FantasiaCarnaval(Item):
    def __init__(self, pos):
        super().__init__("Máscara de Carnaval", pos, 'FantasiaVampiro 19x25.png', 1, 19, 25)

    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        professor.tipo = 'vampiro ' #troca a fantasia
        professor.invisivel = True
        professor.tempo_invisivel = pygame.time.get_ticks() + 8000 # 8 segundos de invisibilidade
        professor.image.set_alpha(128) # Fica semitransparente

class Parede(pygame.sprite.Sprite):
    """Classe para as paredes do labirinto."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.image.fill(AZUL_CIN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image) #Para não empacar nas paredes, o contato será somente com pixel direto

# --- Funções Auxiliares ---

def desenhar_texto(texto, fonte, cor, superficie, x, y, centro=False):
    """Função para desenhar texto na tela."""
    objeto_texto = fonte.render(texto, True, cor)
    rect_texto = objeto_texto.get_rect()
    if centro:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    superficie.blit(objeto_texto, rect_texto)

def encontrar_posicoes_acessiveis(layout, inicio_i, inicio_j):
    """Encontra todas as posições acessíveis a partir de um ponto inicial usando BFS."""
    fila = [(inicio_i, inicio_j)]
    visitados = set([(inicio_i, inicio_j)])
    acessiveis = []

    while fila:
        i, j = fila.pop(0)
        
        # Se for um corredor, adiciona às posições acessíveis para spawn de itens
        if layout[i][j] == 'C':
            x = j * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            y = i * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            acessiveis.append((x, y))

        # Verifica os vizinhos (cima, baixo, esquerda, direita)
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj

            # Checa se o vizinho está dentro dos limites do labirinto
            if 0 <= ni < len(layout) and 0 <= nj < len(layout[0]):
                # Checa se não é uma parede e se ainda não foi visitado
                if layout[ni][nj] != 'P' and (ni, nj) not in visitados:
                    visitados.add((ni, nj))
                    fila.append((ni, nj))
    
    return acessiveis

def criar_labirinto():
    """Cria os sprites do labirinto e retorna as posições válidas."""
    paredes = pygame.sprite.Group()
    pos_entrada_rect = None
    pos_saida_rect = None
    pos_entrada_centro = None
    inicio_i, inicio_j = -1, -1 # Coordenadas da matriz para o início do BFS

    for i, linha in enumerate(LAYOUT_LABIRINTO):
        for j, celula in enumerate(linha):
            x, y = j * TAMANHO_BLOCO, i * TAMANHO_BLOCO
            if celula == 'P':
                paredes.add(Parede(x, y))
            elif celula == 'E':
                pos_entrada_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
                pos_entrada_centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
                inicio_i, inicio_j = i, j # Guarda a posição inicial
            elif celula == 'S':
                pos_saida_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

    # Agora, encontra as posições realmente acessíveis
    if inicio_i != -1:
        posicoes_validas = encontrar_posicoes_acessiveis(LAYOUT_LABIRINTO, inicio_i, inicio_j)
    else:
        posicoes_validas = [] # Caso não encontre a entrada

    return paredes, posicoes_validas, pos_entrada_centro, pos_entrada_rect, pos_saida_rect

# --- Jogo Principal ---

def main():
    """Função principal que roda o jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # Fontes
    fonte_grande = pygame.font.Font(None, 74)
    fonte_media = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 36)
    
    # Variáveis de estado do jogo
    estado_jogo = "TELA_INICIAL"
    
    # Loop principal
    while True:
        if estado_jogo == "TELA_INICIAL":
            tela.fill(PRETO)
            desenhar_texto(TITULO_JOGO, fonte_grande, AMARELO, tela, LARGURA_TELA // 2, ALTURA_TELA // 4, True)
            desenhar_texto("Ajude o Prof. Stefan a chegar no Carnaval!", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
            desenhar_texto("Pressione ENTER para começar", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 3 / 4, True)
            desenhar_texto("ESC para sair do jogo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 3 / 4 + 40, True)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        estado_jogo = "JOGANDO"
                        # Reinicia as variáveis do jogo
                        paredes, pos_validas, pos_e_centro, pos_e_rect, pos_s_rect = criar_labirinto()
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
            alunos.update()
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
            tela.fill(PRETO)
            
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
            tela.fill(VERDE)
            desenhar_texto("VOCÊ CONSEGUIU!", fonte_grande, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 3, True)
            desenhar_texto("RUMO AO CARNAVAL!", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
            desenhar_texto("Pressione ENTER para jogar de novo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 2 / 3, True)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado_jogo = "TELA_INICIAL"

        elif estado_jogo == "DERROTA":
            tela.fill(VERMELHO)
            desenhar_texto("TEMPO ESGOTADO!", fonte_grande, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 3, True)
            desenhar_texto("Mais um ano no CIn...", fonte_media, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA // 2, True)
            desenhar_texto("Pressione ENTER para tentar de novo", fonte_pequena, BRANCO, tela, LARGURA_TELA // 2, ALTURA_TELA * 2 / 3, True)
            
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