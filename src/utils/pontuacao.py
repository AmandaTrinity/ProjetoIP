# src/utils/pontuacao.py
import os

# O nome do arquivo é definido aqui, mas será usado a partir da raiz do projeto,
# onde main.py é executado.
ARQUIVO_PONTUACAO = 'melhores_tempos.txt'

def carregar_melhores_tempos():
    """Carrega os dois melhores tempos a partir de um arquivo."""
    if not os.path.exists(ARQUIVO_PONTUACAO):
        return [float('inf'), float('inf')]
    try:
        with open(ARQUIVO_PONTUACAO, 'r') as f:
            tempos = [float(linha.strip()) for linha in f]
            while len(tempos) < 2:
                tempos.append(float('inf'))
            return sorted(tempos)[:2]
    except (ValueError, IndexError):
        return [float('inf'), float('inf')]

def salvar_melhores_tempos(tempos):
    """Salva os dois melhores tempos no arquivo."""
    with open(ARQUIVO_PONTUACAO, 'w') as f:
        for tempo in sorted(tempos)[:2]:
            f.write(f"{tempo}\n")