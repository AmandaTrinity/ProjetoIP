# src/settings.py
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
CINZA = (128, 128, 128)

# Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
LARGURA_BARRA_LATERAL = 200
TAMANHO_BLOCO = 40
LARGURA_TOTAL = LARGURA_TELA + LARGURA_BARRA_LATERAL

# Jogo
TITULO_JOGO = "Jornada para o Carnaval"
FPS = 30
TEMPO_TOTAL_JOGO = 60  # Tempo por fase

# Configurações do Jogador
VELOCIDADE_JOGADOR = 5

# Configurações dos Power-ups (em milissegundos)
DURACAO_BOOST_MS = 5000
DURACAO_INVISIBILIDADE_MS = 8000
DURACAO_PITU_FASE1_MS = 7000
DURACAO_PITU_FASE2_MS = 9000
DURACAO_PITU_FASE3_MS = 11000
TEMPO_TELA_FINAL_MS = 4000 # 4 segundos

# --- Estrutura do Labirinto ---
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

# --- Diretórios de Assets ---
# Identifica o diretório raiz do projeto (JornadaParaOCarnaval/)
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_ASSETS = os.path.join(DIRETORIO_RAIZ, 'assets')
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_ASSETS, 'imagens')
DIRETORIO_SONS = os.path.join(DIRETORIO_ASSETS, 'sons')
DIRETORIO_FONTES = os.path.join(DIRETORIO_ASSETS, 'fontes')

# --- Configuração de Áudio ---
VOLUMES_PADRAO = {'musica': 0.6, 'efeitos': 0.7, 'passos': 0.5}