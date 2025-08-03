# Mirella's Version - Projeto IP
### Relatório pessoal de aprendizado 

## Dia 1: Organização da arquitetura básica

O objetivo inicial era configurar o básico para fazer um jogo.

### O que eu fiz:
- Instalei a biblioteca Pygame usando o terminal.
- Configurei config.py no VS Code.
- Escrevi um código extremamente báscio de criação de uma janela preta.

### O que eu aprendi:
- O que é uma biblioteca e como instalá-la.
- O básico de um programa em Pygame: _pygame.init()_, um loop e _pygame.quit()_.
- A importância do loop de eventos (_for event in pygame.event.get()_) para tornar a janela interativa (permitir que ela seja fechada).

### Desafios que eu superei:
- Dificuldade em trocar de pastas dentro do terminal e encontrar o arquivo correto.

## Dia 2: Aplicando um pouco de POO 

Depois que a janela já estava funcionando, agora eu precisava aprender como criar elementos no jogo (objetos).

### O que eu fiz:
- Criei a classe Jogador, que represeta o personagem.
- Desenhei um jogador extremamente básico (quadrado azul).
- Descobri que AWSD é uma convenção inata da biblioteca pygame e implementei.
- Criei a primeira classe Coletavel.
- Iniciei a modularização dos códigos

### O que eu aprendi:
- A importância das Classes para o manuseamento de Objetos.
- Aprendi que __init__ é o que define as caracteristicas inicias do objeto.
- Diferenciei os dados de um objeto das suas ações.
- Herança: criei uma classe mãe e classes filhas
- A importância de vários branches (modularização )para chegar no resultado desejado

### Desafios que eu superei:
- Sintaxe extremamente diferente do que eu já vi até hoje programando em Python

### Desafios que eu superei:
- Dificuldade em trocar de pastas dentro do terminal e encontrar o arquivo correto.
- Entender por que salvar o código no VS Code não o atualizava automaticamente no GitHub.

## Dia 3: Aplicando um pouco de POO 

Depois de uma reunião em grupo, meus colegas disseram que gostariam de um grande mapa e um foco como uma "câmera" seguindo o jogador.
Além disso, disseram que queriam que o jogador interagisse com uma coordenada (x,y) para iniciar um mini-game e ganhar um coletável, então fui estudar como é possível fazer isso.

### O que eu fiz:
- Estudei como seria a implementação dessa movimentação com câmera.
- Criei a lógica de "coleta por conquista": o coletável só aparece depois de interagir com o PontoDeInteresse.
- Implementei um sistema de mudança de estados para transitar entre a tela do mapa e as telas dos mini-games.

### O que eu aprendi:
- Aprendi que a câmera não é algo inato do Pygame: tive que criar uma lógica.
-  A ideia de mover o "mundo" na direção oposta ao jogador para criar uma ilusão de movimento.
- Aprendi que a partir de agora será necessário tratar com objetos com .sprite
- Como uma simples variável (estado_jogo) pode controlar completamente o que é desenhado e executado na tela.
- __pygame.key.get_pressed()__ x _pygame.KEYDOWN_: andar x interagir
- A remoção de Sprites após a coleta é feita com .kill()

### Desafios que eu superei:
- Muitos conceitos novos e diferentes, demorei um pouco para estudar tudo e entender o que estava fazendo

_Método Feature Branch Workflow._: as ramificações são limitadas ao que é necessário.
	
 	main.py: ramificação principal que não recebe mudanças
	feature.py: para cada nova feature, será criada uma nova ramificação temporária a partir da main

 - O desenvolvimento de funcionalidades fora do código principal é uma prática precavida, pois evita modificações indesejadas nele. Além disso, é mais organizado.
   
_Herança_: as características da mãe são herdadas pelas filhas

	class Coletavel: classe que define as características básicas todo e qualquer coletável do jogo
	class x(Coletavel): classe que define um coletável x para além de suas características básicas comuns
