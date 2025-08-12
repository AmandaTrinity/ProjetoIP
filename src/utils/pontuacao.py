# src/utils/pontuacao.py
import os

# O caminho para o arquivo de pontuação, dentro de uma pasta 'data' na raiz do projeto.
ARQUIVO_PONTUACAO = os.path.join('data', 'melhores_tempos.txt')

def carregar_melhores_tempos():
    """Carrega os dois melhores tempos a partir de um arquivo."""
    if not os.path.exists(ARQUIVO_PONTUACAO):
        return [float('inf'), float('inf')]
    try:
        with open(ARQUIVO_PONTUACAO, 'r') as f:
            # Ignora linhas em branco que poderiam causar um ValueError
            tempos = [float(linha.strip()) for linha in f if linha.strip()]
            while len(tempos) < 2:
                tempos.append(float('inf'))
            return sorted(tempos)[:2]
    except (ValueError, IndexError):
        # Retorna o padrão em caso de arquivo corrompido ou mal formatado
        return [float('inf'), float('inf')]

def salvar_melhores_tempos(tempos):
    """Salva os dois melhores tempos no arquivo, criando o diretório se necessário."""
    try:
        # Garante que o diretório 'data' exista antes de tentar escrever o arquivo
        os.makedirs(os.path.dirname(ARQUIVO_PONTUACAO), exist_ok=True)
        with open(ARQUIVO_PONTUACAO, 'w') as f:
            for tempo in sorted(tempos)[:2]:
                f.write(f"{tempo}\n")
    except IOError as e:
        print(f"Erro ao salvar os melhores tempos em '{ARQUIVO_PONTUACAO}': {e}")