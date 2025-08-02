# Projeto IP

# Organização da arquitetura

_Método Feature Branch Workflow._: as ramificações são limitadas ao que é necessário.
	
 	main.py: ramificação principal que não recebe mudanças
	feature.py: para cada nova feature, será criada uma nova ramificação temporária a partir da main

 - O desenvolvimento de funcionalidades fora do código principal é uma prática precavida, pois evita modificações indesejadas nele. Além disso, é mais organizado.
   
_Herança_: as características da mãe são herdadas pelas filhas

	class Coletavel: classe que define as características básicas todo e qualquer coletável do jogo
	class x(Coletavel): classe que define um coletável x para além de suas características básicas comuns
