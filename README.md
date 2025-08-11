## Jornada para o Carnaval

## Descrição do Projeto:

O nosso projeto é um jogo de labirinto onde o personagem principal, o Professor Stefan, precisa coletar três itens temáticos do Carnaval de Olinda (uma sombrinha de carnaval, uma garrafa de pitu e uma máscara de carnaval) e encontrar a saída do labirinto antes que o tempo acabe. A história gira em torno de um universitário do CIn/UFPE do período 2024.2 que, para ser liberado para o feriado, precisa completar essa jornada carnavalesca dentro da faculdade.

Cada coletável tem uma função especial no jogo. O labirinto, os coletáveis e a saída são gerados aleatoriamente a cada partida, garantindo que cada jogo seja uma experiência nova e divertida.

## Participantes do Projeto:

  * Mirella Laura Fontinelle Martins \<mlfm\>
  * Willian Neves Rupert Jones \<wnrj\>
  * Maria Luísa Brandão Amaral \<mlba\>
  * Maria Eduarda Torres da Costa Lira \<metcl\>
  * Luiz Miguel Freitas da Silva \<lmfs3\>
  * Amanda Trinity Gomes Nascimento \<atgn\>

## Organização e Desenvolvimento de Jogo:

Nosso grupo se dividiu para desenvolver o jogo de maneira mais eficiente. Alguns membros ficaram com a parte de programação do jogo e outros com a parte visual e de animações. Tivemos reuniões online e presenciais para alinhamento de ideias, revisão de código e planejamento. Todos participaram de forma ativa e colaborativa.

## Divisão de Tarefas:

| **Dupla** | **Tarefas** |
| :--- | :--- |
| Amanda Trinity Gomes Nascimento e Willian Neves Rupert Jones | Código principal |
| Maria Eduarda Torres da Costa Lira e Maria Luísa Brandão Amaral | Personagens, sons, cenários e coletáveis |
| Mirella Laura Fontinelle Martins e Luiz Miguel Freitas da Silva | Tela de início e tela final |

## Ferramentas Utilizadas:

  * **Pygame**: biblioteca para jogos 2D em Python
  * **Pyamaze**: geração do labirinto
  * **Piskel**: criação das sprites e animações
  * **VSCode**: ambiente de programação
  * **GitHub**: versionamento de código e colaboração

## Arquitetura do Projeto

```bash
PROJETO/                          
│── assets/                    # Recursos estáticos do projeto
│   ├── imagens/               # Imagens usadas no projeto
│   │   ├── sprites/           # Sprites utilizados no jogo
│   ├── sons/                  # Arquivos de áudio (efeitos sonoros e músicas)
│   
│── src/                       # Código fonte do projeto
│   ├── coletaveis/            # Módulo para objetos coletáveis no jogo
│   │   ├── coletaveis.py      # Definição dos objetos coletáveis
│   │   ├── fantasiaCarnaval.py # Coletável: fantasia de carnaval
│   │   ├── garrafaPitu.py     # Coletável: garrafa de Pitu
│   │   ├── sombrinha.py       # Coletável: sombrinha
│   ├── labirinto/             # Lógica do labirinto
│   │   ├── labirinto.py       # Definição e lógica do labirinto
│   ├── movimento/             # Lógica de movimentação dos personagens
│   │   ├── movimento.py       # Movimentação dos personagens no jogo
│   ├── personagens/           # Módulo dos personagens do jogo
│   │   ├── aluno.py           # Definição do personagem aluno
│   │   ├── professor.py       # Definição do personagem professor
│   ├── telas/                 # Definição das telas e interfaces gráficas
│   │   ├── telas.py           # Lógica de renderização das telas
│   ├── utils/                 # Funções auxiliares e utilitárias
│   │   ├── audio.py           # Manipulação de áudio (efeitos sonoros e músicas)
│   │   ├── constantes.py      # Constantes utilizadas no código
│   │   ├── desenho.py         # Funções de desenho gráfico
│   │   ├── setup.py           # Configurações iniciais do projeto
│   
│── main                   # Arquivo principal do projeto
│
│── package.json               # Arquivo de configuração do projeto (scripts, etc.)
```
## Principais Objetivos do Projeto:

  * Criar um jogo funcional usando Pygame e Pyamaze
  * Aplicar os conceitos de programação aprendidos
  * Trabalhar em equipe para desenvolver um projeto completo

Este README será atualizado conforme o desenvolvimento do jogo avança.

# Organização da arquitetura

_Método Feature Branch Workflow._: as ramificações são limitadas ao que é necessário.
	
 	main.py: ramificação principal que não recebe mudanças
	feature.py: para cada nova feature, será criada uma nova ramificação temporária a partir da main

 - O desenvolvimento de funcionalidades fora do código principal é uma prática precavida, pois evita modificações indesejadas nele. Além disso, é mais organizado.
   
