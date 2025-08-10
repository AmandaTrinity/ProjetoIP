import pygame
import os
from src.utils.constantes import IMAGENS_DIR, TAMANHO_BLOCO, AMARELO
from src.utils.audio import som_andando

class Professor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- Lógica de Animação ---
        self.animacoes = {}
        self.parado = {}
        try:
            frames_normais_direita = [] #Adiciona imagens andando para direita
            for i in range(4):
                nome_do_arquivo = f"stefan_direita{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                                
                frame_direita = pygame.image.load(caminho_completo).convert_alpha()
                frame_direita = pygame.transform.scale(frame_direita, (40, 40))
                frames_normais_direita.append(frame_direita)

            self.animacoes['normal direita'] = frames_normais_direita
            frames_normais_esquerda = []
            for i in range(4): #Adiciona imagens andando para esquerda
                nome_do_arquivo = f"stefan_esquerda{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                                
                frame_esquerda = pygame.image.load(caminho_completo).convert_alpha()
                frame_esquerda = pygame.transform.scale(frame_esquerda, (40, 40))
                frames_normais_esquerda.append(frame_esquerda)

            self.animacoes['normal esquerda'] = frames_normais_esquerda
            self.parado = {'normal direita': self.animacoes['normal direita'][0], 'normal esquerda': self.animacoes['normal esquerda'][0]}
            
            #Carregar imagens fantasiados
            vampiro_direita_lista=[]
            for i in range(4):
                nome_do_arquivo = f"stefanvampiro_direita{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                                
                vampiro_direita = pygame.image.load(caminho_completo).convert_alpha()
                vampiro_direita = pygame.transform.scale(vampiro_direita, (40, 40))
                vampiro_direita_lista.append(vampiro_direita)
            self.animacoes['vampiro direita'] = vampiro_direita_lista

            vampiro_esquerda_lista=[]
            for i in range(4):
                nome_do_arquivo = f"stefanvampiroesqueda_{i}.png"
                caminho_completo = os.path.join(IMAGENS_DIR, nome_do_arquivo)
                                
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
        self.som_andando_tocando = False #para o som dele andando parar somente quando ele parar e só iniciar quando ele começar a andar


    def mover(self, direcao_x, direcao_y, paredes):
        # O método mover SÓ se preocupa com o movimento.
        # Se o personagem se moveu (dx ou dy não são zero), ativamos a animação.
        if direcao_x != 0 or direcao_y != 0:
            self.animar_agora = True
        else:
            self.animar_agora = False

        #Lógica de direção
        if direcao_x > 0:
            self.direcao='direita'
        elif direcao_x < 0:
            self.direcao='esquerda'

        self.rect.x += direcao_x * self.velocidade
        for parede in paredes:
            if pygame.sprite.collide_mask(self, parede):
                if direcao_x > 0: self.rect.right = parede.rect.left
                if direcao_x < 0: self.rect.left = parede.rect.right
        
        self.rect.y += direcao_y * self.velocidade
        for parede in paredes:
            if pygame.sprite.collide_mask(self, parede):
                if direcao_y > 0: self.rect.bottom = parede.rect.top
                if direcao_y < 0: self.rect.top = parede.rect.bottom

    def update(self, tempo_atual):
        estado_animacao_atual=self.tipo + self.direcao

        #Lógica para o som de andar
        if self.animar_agora and not self.som_andando_tocando: #Só inicia se não estava tocando
            som_andando.play(-1) #Toca o som em loop (-1)
            self.som_andando_tocando = True
        elif not self.animar_agora and self.som_andando_tocando: #parou de andar
            som_andando.stop()
            self.som_andando_tocando=False

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
