## Jornada para o Carnaval

## Descrição do Projeto:

O nosso projeto é um jogo de labirinto onde o personagem principal, o Professor Stefan, precisa coletar três itens temáticos do Carnaval de Olinda (uma sombrinha de carnaval, uma garrafa de pitu e uma máscara de carnaval) e encontrar a saída do labirinto antes que o tempo acabe. A história gira em torno de um universitário do CIn/UFPE do período 2024.2 que, para ser liberado para o feriado, precisa completar essa jornada carnavalesca dentro da faculdade.

Cada coletável tem uma função especial no jogo (a ser definida). O labirinto, os coletáveis e a saída são gerados aleatoriamente a cada partida, garantindo que cada jogo seja uma experiência nova e divertida.

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

### src/funcoes\_labirinto.py

Responsável por gerar o labirinto, posicionar a porta de saída, definir as cores de fundo e das paredes.

### src/funcoes\_coletaveis.py

Gera os coletáveis (sombrinha, pitu, máscara), define suas funções e verifica coleta e vitória.

### src/funcoes\_personagem.py

Controla as animações, direções, movimentos e eventos do personagem (Stefan).

### src/funcoes\_telas\_jogo.py

Carrega a tela inicial e a tela de finalização do jogo.

### assets/

Contém imagens, sons e sprites usados no jogo.

## Principais Objetivos do Projeto:

  * Criar um jogo funcional usando Pygame e Pyamaze
  * Aplicar os conceitos de programação aprendidos
  * Trabalhar em equipe para desenvolver um projeto completo

Este README será atualizado conforme o desenvolvimento do jogo avança.


# Projeto Introdução a Programação

# Organização da arquitetura

_Método Feature Branch Workflow._: as ramificações são limitadas ao que é necessário.
	
 	main.py: ramificação principal que não recebe mudanças
	feature.py: para cada nova feature, será criada uma nova ramificação temporária a partir da main

 - O desenvolvimento de funcionalidades fora do código principal é uma prática precavida, pois evita modificações indesejadas nele. Além disso, é mais organizado.
   