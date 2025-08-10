import pygame
import os

# Caminhos para Assets
# Define o caminho raiz do projeto subindo dois níveis
# a partir do diretório deste arquivo (src/utils)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
IMAGENS_DIR = os.path.join(ASSETS_DIR, 'imagens')
SONS_DIR = os.path.join(ASSETS_DIR, 'sons')
SPRITES_DIR = os.path.join(IMAGENS_DIR, 'sprites') 

pygame.init()
pygame.mixer.init()

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
CINZA = (128,128,128)

# Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_BLOCO = 40

# Jogo
TITULO_JOGO = "Jornada para o Carnaval"
FPS = 30
TEMPO_TOTAL_JOGO = 60  # em segundos

# Estrutura do Labirinto
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