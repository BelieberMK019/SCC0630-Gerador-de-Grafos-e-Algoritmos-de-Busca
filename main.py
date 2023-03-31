import random
import math
import time
import matplotlib.pyplot as plt
import os

##Classe que representa um ponto, com coordenadas x e y
class Point: 
	#Construtor
	def __init__(self , x , y):
		self.x = x
		self.y = y
	#String
	def __str__(self):
		escrita = "({x:.3f} , {y:.3f})".format(x = self.x , y = self.y)
		return escrita

##Classe que representa um nó do grafo, com seu próprio valor de ponto e referências aos nós com que ele está ligado
class Node:
	#Construtor
	def __init__(self , ponto):
		self.ponto = ponto
		self.conexoes = []
	#String
	def __str__(self):
		escrita = "PONTO:\n" + str(self.ponto) + "\n"
		escrita = escrita + "CONEXÕES:\n"
		for conexao in self.conexoes:
			escrita = escrita + str(conexao.ponto) + "\n"
		return escrita
	#Método que acrescenta uma conexão ao nó
	def addConexao(self , no):
		self.conexoes.append(no)

######################### FUNÇÕES DE GERAR GRAFOS #############################

#Função que calcula a distância entre dois objetos ponto
def dist(p1 , p2):
	return math.sqrt(math.pow((p1.x-p2.x),2)+math.pow((p1.y-p2.y),2))

##Função que cria um grafo KNN para determinados valores de V e K
def grafoKNN(v, k):
	#Criando V pontos em posições aleatórias
	pontos = []
	for i in range(v):
		pontos.append(Point(random.random()*v , random.random()*v))
		
	#Criando V nós, cada um com um valor de ponto criado acima
	nos = []
	for i in range(v):
		nos.append(Node(pontos[i])) 
	
	#Decidindo quais vão ser as conexões para cada nó criado
	conexoes = []
	for i in range(v):
		#Calculando as distâncias entre o nó tratado atualmente e todos os outros
		tamanhos = []
		for j in range(v):
			if (j != i):
				tamanhos.append(dist(pontos[i], pontos[j]))
			else:
				tamanhos.append(v*math.sqrt(2)+1) #Distância entre "um no e ele mesmo" é sempre a maior possível para o cenário
		
		#Escolhendo os nós às K menores distâncias como conexões
		aux = []
		for j in range(k):
			menor = i
			for q in range(v):
				if (tamanhos[q] < tamanhos[menor]):
					jaTem = False
					for o in range(j):
						if (q == aux[o]): #Evita que haja dois nós repetidos como conexão de um mesmo nó
							jaTem = True 
							break
					if ((not jaTem)):
						menor = q
			aux.append(menor)
		conexoes.append(aux)

	#Adicionando os nós escolhidos como conexão aos nós respectivos
	for i in range(v):
		for j in range(k):
			nos[i].addConexao(nos[conexoes[i][j]])
			jaTem = False
			#Garante a reciprocidade, quando um nó tem o outro em sua lista de conexões, o outro nó também deve ter ele
			for conexao in nos[conexoes[i][j]].conexoes:
				if (conexao == nos[i]):
					jaTem = True
			if (not jaTem):
				nos[conexoes[i][j]].addConexao(nos[i])
	return nos

##Função que cria um grafo Random para determinados valores de V e K
def grafoRandom(v, k):
	#Criando V pontos em posições aleatórias
	pontos = []
	for i in range(v):
		pontos.append(Point(random.random()*v , random.random()*v))

	#Criando V nós, cada um com um valor de ponto criado acima
	nos = []
	for i in range(v):
		nos.append(Node(pontos[i])) 

	#Decidindo quais vão ser as conexões para cada nó criado
	conexoes = []
	for i in range(v):

		#Escolhendo K nós aleatoriamente como conexões
		aux = []
		for j in range(k):
			while (True):
				indice = int(random.random()*v)
				if (indice == i): #Evita que um nó se conecte com si mesmo
					continue
				jaTem = False
				for q in range(j):
					if (indice == aux[q]): #Evita que haja dois nós repetidos como conexão de um mesmo nó
						jaTem = True
						break
				if ((not jaTem)):
					break
			aux.append(indice)
		conexoes.append(aux)
	
	#Adicionando os nós escolhidos como conexão aos nós respectivos
	for i in range(v):
		for j in range(k):
			nos[i].addConexao(nos[conexoes[i][j]])
			jaTem = False
			#Garante a reciprocidade, quando um nó tem o outro em sua lista de conexões, o outro nó também deve ter ele
			for conexao in nos[conexoes[i][j]].conexoes:
				if (conexao == nos[i]):
					jaTem = True
			if (not jaTem):
				nos[conexoes[i][j]].addConexao(nos[i])
	return nos

#Função que gera um grafo do tipo escolhido pela variável qual
def geradorDeGrafo(v , k , qual):
	if (qual == 1):
		print("\nGerando o Grafo KNN com as especificações fornecidas...")
		return grafoKNN(v, k)
	else:
		print("\nGerando o Grafo Random com as especificações fornecidas...")
		return grafoRandom(v, k)

############################# FUNÇÕES DE PLOT ###############################

#Função que plota o grafo, preparando-o para ser mostrado
def plotGrafo(nos, exibirIndice):
	for no in nos:
		for conexao in no.conexoes:
			x = []
			y = []
			x.append(no.ponto.x)
			y.append(no.ponto.y)
			x.append(conexao.ponto.x)
			y.append(conexao.ponto.y)
			plt.plot(x, y, "b-", linewidth=0.1)
	x = []
	y = []
	for no in nos:
		x.append(no.ponto.x)
		y.append(no.ponto.y)
	plt.plot(x, y, "go", markersize=2)
	delta = 0.1
	if (exibirIndice):
		for i in range(len(nos)):
			plt.text(nos[i].ponto.x+delta, nos[i].ponto.y+delta, str(i+1), fontsize=8)

#Função que plota o caminho sobre o grafo
def plotCaminho(caminho):
	x = caminho[0].ponto.x
	y = caminho[0].ponto.y
	plt.plot(x, y, "ko", markersize=6)
	for i in range(len(caminho)-1):
		x = [caminho[i].ponto.x , caminho[i+1].ponto.x]
		y = [caminho[i].ponto.y , caminho[i+1].ponto.y]
		plt.plot(x, y, "r-", linewidth=0.5)
		if (i+1 != (len(caminho)-1)):
			x = caminho[i+1].ponto.x
			y = caminho[i+1].ponto.y
			plt.plot(x, y, "ro", markersize=4)
	x = caminho[len(caminho)-1].ponto.x
	y = caminho[len(caminho)-1].ponto.y
	plt.plot(x, y, "ko", markersize=6)

#Função que plota o caminho sobre o grafo, em uma animação (no replit)
def plotCaminhoAnim(caminho):
	x = caminho[0].ponto.x
	y = caminho[0].ponto.y
	plt.plot(x, y, "ko", markersize=6)
	plt.pause(0.0001)
	for i in range(len(caminho)-1):
		x = [caminho[i].ponto.x , caminho[i+1].ponto.x]
		y = [caminho[i].ponto.y , caminho[i+1].ponto.y]
		plt.plot(x, y, "r-", linewidth=0.5)
		plt.pause(0.0001)
		if (i+1 != (len(caminho)-1)):
			x = caminho[i+1].ponto.x
			y = caminho[i+1].ponto.y
			plt.plot(x, y, "ro", markersize=4)
			plt.pause(0.0001)
	x = caminho[len(caminho)-1].ponto.x
	y = caminho[len(caminho)-1].ponto.y
	plt.plot(x, y, "ko", markersize=6)
	plt.pause(0.0001)

#Função que mostra o grafo após prepará-lo com a plotGrafo()
def exibirGrafo(v , qual):
	if (qual == 1):
		plt.suptitle("Grafo KNN")
	else:
		plt.suptitle("Grafo Random")
	plt.axis([0, v, 0, v])
	plt.ylabel("y")
	plt.xlabel("x")
	plt.ion()
	plt.axis("square")
	plt.show()

############################# FUNÇÕES DE INPUT ################################

#Função que pede uma entrada de V, faz o tratamento de erros
def setV():
	while True:
		try:
			v = int(input("\nInsira um valor para V: "))
			if (v > 0):
				return v
			else:
				raise Exception()
		except:
			print("Valor inválido!")

#Função que pede uma entrada de K, faz o tratamento de erros
def setK(v):
	while True:
		try:
			k = int(input("Insira um valor para K: "))
			if (k < v and k > 0):
				return k
			else:
				raise Exception()
		except:
			print("Valor inválido!")

#Função que pede uma entrada de qual o tipo de grafo, faz o tratamento de erros
def setQualGrafo():
	while True:
		try:
			qual = int(input("Insira o número da opção desejada: "))
			if (qual > 0 and qual < 3):
				return qual
			else:
				raise Exception()
		except:
			print("Valor inválido!")

#Função que pede uma entrada de qual o tipo de busca, faz o tratamento de erros
def setQualBusca():
	while True:
		try:
			qual = int(input("Insira o número da opção desejada: "));
			if (qual > 0 and qual < 7):
				return qual
			else:
				raise Exception()
		except:
			print("Índice Inválido!")

#Função que pede uma entrada de índice para ponto inicial, faz o tratamento de erros
def setPontoInicial(max):
	while True:
		try:
			p = int(input("Insira o índice do ponto de partida: "));
			if (p > 0 and p <= max):
				return p
			else:
				raise Exception()
		except:
			print("Índice Inválido!")

#Função que pede uma entrada de índice para ponto final, faz o tratamento de erros
def setPontoFinal(max):
	while True:
		try:
			p = int(input("Insira o índice do ponto de chegada: "));
			if (p > 0 and p <= max):
				return p
			else:
				raise Exception()
		except:
			print("Índice Inválido!")

############################# FUNÇÕES DE BUSCA ################################

##Função que realiza a busca em profundidade
def buscaProfundidade(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]
		
		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
		#Adicionando os novos nós no início da lista de testes (pois é uma busca em profundidade)
		nosParaOlhar = novosNos + nosParaOlhar[1:]
		caminhos = novosCaminhos + caminhos[1:]

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os novos nós que acabaram de ser colocados (níveis mais altos) serão os mantidos
		aux1 = []
		aux2 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]
		
		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

##Função que realiza a busca em largura, garantindo um caminho passando pelo menor número de nós possível
def buscaLarguraNo(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]

		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
		#Adicionando os novos nós no final da lista de testes (pois é uma busca em largura)
		nosParaOlhar = nosParaOlhar[1:] + novosNos
		caminhos = caminhos[1:] + novosCaminhos

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os nós que estão na lista a mais tempo (níveis mais baixos) serão os mantidos
		aux1 = []
		aux2 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]

		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

##Função que realiza a busca em largura modificada, garantindo um caminho percorrendo a menor distância possível
def buscaLarguraDist(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]
	g = [0]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]

		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		novosGs = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
				novosGs.append(g[0] + dist(nosParaOlhar[0].ponto , conexao.ponto))
		#Adicionando os novos nós no final da lista de testes
		nosParaOlhar = nosParaOlhar[1:] + novosNos
		caminhos = caminhos[1:] + novosCaminhos
		g = g[1:] + novosGs

		#Ordenando a lista de nós para testar de acordo com o G de cada nó
		for i in range(1 , len(nosParaOlhar)):
			noAtual = nosParaOlhar[i]
			caminhoAtual = caminhos[i]
			gAtual = g[i]
			q = 0
			for q in range(i-1 , -1 , -1):
				if (g[q] <= gAtual):
					break
				nosParaOlhar[q+1] = nosParaOlhar[q]
				caminhos[q+1] = caminhos[q]
				g[q+1] = g[q]
			nosParaOlhar[q+1] = noAtual
			caminhos[q+1] = caminhoAtual
			g[q+1] = gAtual

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os nós que possuem o menor G (menor distância percorrida) serão os mantidos
		aux1 = []
		aux2 = []
		aux3 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
				aux3.append(g[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]
		g = aux3[:]

		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

#Função que retorna a estimativa otimista para chegar ao nó final a partir de um dado nó
def h(no1 , noFinal):
	return dist(no1.ponto, noFinal.ponto)

##Função que realiza a busca best first
def buscaBestFirst(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]
	f = [h(noInicial, noFinal)]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]

		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		novosFs = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
				novosFs.append(h(conexao , noFinal))
		#Adicionando os novos nós no final da lista de testes
		nosParaOlhar = nosParaOlhar[1:] + novosNos
		caminhos = caminhos[1:] + novosCaminhos
		f = f[1:] + novosFs

		#Ordenando a lista de nós para testar de acordo com o F de cada nó
		for i in range(1 , len(nosParaOlhar)):
			noAtual = nosParaOlhar[i]
			caminhoAtual = caminhos[i]
			fAtual = f[i]
			q = 0
			for q in range(i-1 , -1 , -1):
				if (f[q] <= fAtual):
					break
				nosParaOlhar[q+1] = nosParaOlhar[q]
				caminhos[q+1] = caminhos[q]
				f[q+1] = f[q]
			nosParaOlhar[q+1] = noAtual
			caminhos[q+1] = caminhoAtual
			f[q+1] = fAtual

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os nós que possuem o menor F (menor estimativa para alcançar o nó final) serão os mantidos
		aux1 = []
		aux2 = []
		aux3 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
				aux3.append(f[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]
		f = aux3[:]

		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

##Função que realiza a busca heurística com o algoritmo A com heurística pessimista (10*distancia)
def buscaA(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]
	g = [0]
	f = [10*h(noInicial, noFinal)]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]

		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		novosGs = []
		novosFs = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
				novosGs.append(g[0] + dist(nosParaOlhar[0].ponto , conexao.ponto))
				novosFs.append(g[0] + dist(nosParaOlhar[0].ponto , conexao.ponto) + 10*h(conexao , noFinal))
		#Adicionando os novos nós no final da lista de testes
		nosParaOlhar = nosParaOlhar[1:] + novosNos
		caminhos = caminhos[1:] + novosCaminhos
		g = g[1:] + novosGs
		f = f[1:] + novosFs

		#Ordenando a lista de nós para testar de acordo com o F de cada nó
		for i in range(1 , len(nosParaOlhar)):
			noAtual = nosParaOlhar[i]
			caminhoAtual = caminhos[i]
			gAtual = g[i]
			fAtual = f[i]
			q = 0
			for q in range(i-1 , -1 , -1):
				if (f[q] <= fAtual):
					break
				nosParaOlhar[q+1] = nosParaOlhar[q]
				caminhos[q+1] = caminhos[q]
				g[q+1] = g[q]
				f[q+1] = f[q]
			nosParaOlhar[q+1] = noAtual
			caminhos[q+1] = caminhoAtual
			g[q+1] = gAtual
			f[q+1] = fAtual

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os nós que possuem o menor F (menor distância percorrida + estimativa para alcançar o nó final) serão os mantidos
		aux1 = []
		aux2 = []
		aux3 = []
		aux4 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
				aux3.append(g[i])
				aux4.append(f[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]
		g = aux3[:]
		f = aux4[:]

		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

##Função que realiza a busca heurística com o algoritmo A*, garantindo um caminho percorrendo a menor distância possível
def buscaAEstrela(noInicial , noFinal):
	#Inicializando as variáveis utilizadas
	nosParaOlhar = [noInicial]
	caminhos = [[noInicial]]
	g = [0]
	f = [h(noInicial, noFinal)]

	while(True):
		if (nosParaOlhar[0] == noFinal): #Caso final da busca => ACHOU
			return caminhos[0]

		#Adicionando as conexões do nó testado à lista de possíveis testes
		novosNos = []
		novosCaminhos = []
		novosGs = []
		novosFs = []
		for conexao in nosParaOlhar[0].conexoes:
			jaTem = False
			for no in caminhos[0]:
				if(conexao == no): #Evita que a busca entre em loop
					jaTem = True
					break
			if(not jaTem):
				novosNos.append(conexao)
				novosCaminhos.append(caminhos[0] + [conexao])
				novosGs.append(g[0] + dist(nosParaOlhar[0].ponto , conexao.ponto))
				novosFs.append(g[0] + dist(nosParaOlhar[0].ponto , conexao.ponto) + h(conexao , noFinal))
		#Adicionando os novos nós no final da lista de testes
		nosParaOlhar = nosParaOlhar[1:] + novosNos
		caminhos = caminhos[1:] + novosCaminhos
		g = g[1:] + novosGs
		f = f[1:] + novosFs

		#Ordenando a lista de nós para testar de acordo com o F de cada nó
		for i in range(1 , len(nosParaOlhar)):
			noAtual = nosParaOlhar[i]
			caminhoAtual = caminhos[i]
			gAtual = g[i]
			fAtual = f[i]
			q = 0
			for q in range(i-1 , -1 , -1):
				if (f[q] <= fAtual):
					break
				nosParaOlhar[q+1] = nosParaOlhar[q]
				caminhos[q+1] = caminhos[q]
				g[q+1] = g[q]
				f[q+1] = f[q]
			nosParaOlhar[q+1] = noAtual
			caminhos[q+1] = caminhoAtual
			g[q+1] = gAtual
			f[q+1] = fAtual

		#Retirando duplicatas da lista, pois os caminhos através de um mesmo nó não precisam ser testados mais de uma vez, no caso de duplicatas, mantemos o que aparece primeiro na lista, nesse caso, os nós que possuem o menor F (menor distância percorrida + estimativa para alcançar o nó final) serão os mantidos
		aux1 = []
		aux2 = []
		aux3 = []
		aux4 = []
		for i in range(len(nosParaOlhar)):	
			if nosParaOlhar[i] not in aux1:
				aux1.append(nosParaOlhar[i])
				aux2.append(caminhos[i])
				aux3.append(g[i])
				aux4.append(f[i])
		nosParaOlhar = aux1[:]
		caminhos = aux2[:]
		g = aux3[:]
		f = aux4[:]

		#Caso acabem os nós para testar, a busca FALHOU
		if len(nosParaOlhar) == 0:
			break

#Função que calcula o comprimento de um determinado caminho pelo grafo
def calcularComprimento(caminho):
	d = 0;
	for i in range(len(caminho)-1):
		d += dist(caminho[i].ponto, caminho[i+1].ponto)
	return d

#Função que realiza a busca do tipo escolhido pela variável qual, além de contar o tempo de execução dessa busca
def iniciarBusca(noInicial , noFinal , qual):
	caminho = []
	inicio = time.time()
	if(qual == 1):
		print("\nIniciando busca em profundidade...")
		caminho = buscaProfundidade(noInicial, noFinal)
	elif(qual == 2):
		print("\nIniciando busca em largura pela quantidade de pontos...")
		caminho = buscaLarguraNo(noInicial, noFinal)
	elif(qual == 3):
		print("\nIniciando busca em largura pela distância...")
		caminho = buscaLarguraDist(noInicial, noFinal)
	elif(qual == 4):
		print("\nIniciando busca best first...")
		caminho = buscaBestFirst(noInicial, noFinal)
	elif(qual == 5):
		print("\nIniciando busca heurística A...")
		caminho = buscaA(noInicial, noFinal)
	elif(qual == 6):
		print("\nIniciando busca heurística A*...")
		caminho = buscaAEstrela(noInicial, noFinal)
	fim = time.time()
	print("...Busca finalizada!")
	print("Duração: ", fim - inicio, " segundos")
	return caminho

#Função que realiza a busca do tipo escolhido pela variável qual, além de contar o tempo de execução dessa busca, mas sem realizar nenhum print, para ser utilizada na função comparaMetodos
def iniciarBuscaAuto(noInicial , noFinal , qual):
	caminho = []
	inicio = time.time()
	if(qual == 1):
		caminho = buscaProfundidade(noInicial, noFinal)
	elif(qual == 2):
		caminho = buscaLarguraNo(noInicial, noFinal)
	elif(qual == 3):
		caminho = buscaLarguraDist(noInicial, noFinal)
	elif(qual == 4):
		caminho = buscaBestFirst(noInicial, noFinal)
	elif(qual == 5):
		caminho = buscaA(noInicial, noFinal)
	elif(qual == 6):
		caminho = buscaAEstrela(noInicial, noFinal)
	fim = time.time()
	tempo = fim - inicio	
	return [caminho , tempo]

############################ FUNÇÕES DE SELEÇÃO ###############################

#Função chamada para possibilitar a seleção do tipo de grafo
def seletorDeGrafo():
	print("Qual tipo de grafo você deseja criar?")
	print("(1) Grafo KNN")
	print("(2) Grafo Random")
	qualGrafo = setQualGrafo()
	return qualGrafo

#Função chamada para possibilitar a seleção do tipo de busca
def seletorDeBusca():
	print("Qual busca você quer realizar?")
	print("(1) Busca em Profundidade")
	print("(2) Busca em Largura pela quantidade de pontos")
	print("(3) Busca em Largura pela distância")
	print("(4) Busca Best First")
	print("(5) Busca Heurística A")
	print("(6) Busca Heurística A*")
	qualBusca = setQualBusca()
	return qualBusca

############################## FUNÇÕES DE AÇÃO ################################

##Função utilizada para testar os métodos e gerar as figuras e animações dos grafos
def testaMetodos():
	print("***** Início do Programa *****")

	#Definindo o tipo de grafo
	qualGrafo = seletorDeGrafo()

	#Definindo os valores de V e K
	v = setV()
	k = setK(v)
	
	#Gerando o grafo desejado e desenhando ele
	nos = geradorDeGrafo(v , k , qualGrafo)
	plotGrafo(nos , False)
	exibirGrafo(v , qualGrafo)
	print("...Grafo gerado\n")

	while(True):
		#Definindo o tipo de busca
		qualBusca = seletorDeBusca()

		#Desenhando o grafo com índices
		print("\nAdicionaremos o índice de cada nó à imagem do grafo para que você possa escolher os pontos de partida e chegada da busca (use o zoom se necessário)...\n")
		plt.close()
		plotGrafo(nos, True)
		exibirGrafo(v , qualGrafo)

		#Definindo os nós inicial e final da busca
		indiceNoInicial = setPontoInicial(v)
		indiceNoFinal = setPontoFinal(v)

		#Realizando a busca e desenhando o caminho obtido
		caminho = iniciarBusca(nos[indiceNoInicial-1] , nos[indiceNoFinal-1] , qualBusca)
		if (caminho == None):
			print("...Não há um caminho entre os dois pontos\n")
		else:
			print("...O algoritmo encontrou esse caminho mostrado na imagem\n")
			plt.close()
			plotGrafo(nos, False)
			exibirGrafo(v , qualGrafo)
			plotCaminhoAnim(caminho)

		#Permitindo a opção de realizar outra busca ou parar por aí
		dnv = input("Digite '1' para tentar outra busca ou qualquer outra coisa para sair: ")
		print()
		if (dnv != "1"):
			print("...Saindo do programa")
			break

#Função que define nó inicial e final aleatoriamente para serem usados na comparaMetodos
def definirNos(nos):
	v = len(nos)
	indiceInicial = int(random.random()*v)
	raio = v/3
	indiceFinal = int(random.random()*v)
	while (True):
		if (dist(nos[indiceInicial].ponto, nos[indiceFinal].ponto) > raio):
			break
		else:
			indiceFinal += 1
			indiceFinal = indiceFinal % v
	return [nos[indiceInicial], nos[indiceFinal]]

##Função utilizada para comparar os métodos de busca para grafos KNN em termos de tempo de execução, comprimento de caminho e número de nós percorridos, podendo realizar a comparação para N exemplos de grafos e tirar a média ao final
def comparaMetodosKNN(v , k , n):
	print("V = " , str(v) , " ; K = " , str(k))

	#Inicializando os guardadores de dados para a comparação dos métodos
	tamanhosNo = [[] , [] , [] , [] , [] , []]
	tamanhosDist = [[] , [] , [] , [] , [] , []]
	tempos = [[] , [] , [] , [] , [] , []]
	naoEncontrou = 0

	if not os.path.isdir(".//GraficosKNN"):
		os.mkdir(".//GraficosKNN")

	#Computando os dados para cada exemplo de grafo
	i = 0
	while (i < n):
		#Gerando o grafo
		nos = grafoKNN(v , k)	

		#Definindo nós inicial e final da busca	
		[noInicial, noFinal] = definirNos(nos)

		#Computando os dados para cada tipo de busca
		for j in range(6):
			print("i = " , str(i) , " ; j = " , str(j))

			#Realiza a busca
			[caminho, tempo] = iniciarBuscaAuto(noInicial , noFinal , j+1)

			#Caso não exista um caminho entre os nós, cancela esse grafo e gera outro
			if (caminho == None):
				naoEncontrou += 1
				i -= 1
				break

			#Guarda os dados calculados
			tamanhosNo[j].append(len(caminho))
			tamanhosDist[j].append(calcularComprimento(caminho))
			tempos[j].append(tempo)

			#Salva imagens do primeiro exemplo de grafo gerado, com os caminhos encontrados por cada método desenhados
			if (i == 0):
				plotGrafo(nos, False)
				plotCaminho(caminho)
				if(j == 0):
					plt.suptitle("Busca em Profundidade")
					if not os.path.isdir(".//GraficosKNN//Profundidade"):
						os.mkdir(".//GraficosKNN//Profundidade")
					plt.savefig("GraficosKNN//Profundidade//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 1):
					plt.suptitle("Busca em Largura por pontos")
					if not os.path.isdir(".//GraficosKNN//LarguraNo"):
						os.mkdir(".//GraficosKNN//LarguraNo")
					plt.savefig("GraficosKNN//LarguraNo//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 2):
					plt.suptitle("Busca em Largura por distância")
					if not os.path.isdir(".//GraficosKNN//LarguraDist"):
						os.mkdir(".//GraficosKNN//LarguraDist")
					plt.savefig("GraficosKNN//LarguraDist//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 3):
					plt.suptitle("Busca Best First")
					if not os.path.isdir(".//GraficosKNN//BestFirst"):
						os.mkdir(".//GraficosKNN//BestFirst")
					plt.savefig("GraficosKNN//BestFirst//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 4):
					plt.suptitle("Busca Heurística A")
					if not os.path.isdir(".//GraficosKNN//A"):
						os.mkdir(".//GraficosKNN//A")
					plt.savefig("GraficosKNN//A//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 5):
					plt.suptitle("Busca Heurística A*")
					if not os.path.isdir(".//GraficosKNN//AEstrela"):
						os.mkdir(".//GraficosKNN//AEstrela")
					plt.savefig("GraficosKNN//AEstrela//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				plt.close()
		i += 1

	#Salva os dados computados em um arquivo de texto
	frases = []
	frases.append("Número de vezes que não foi encontrado caminho: " + str(naoEncontrou) + "\n")
	frases.append("\n")
	frases.append("Número de Nós Percorridos\tComprimento do Caminho\tTempo de Execução\n")
	for j in range(6):
		frases.append("\n")
		if(j == 0):
			frases.append("Busca em Profundidade\n")
		elif(j == 1):
			frases.append("Busca em Largura por pontos\n")
		elif(j == 2):
			frases.append("Busca em Largura por distância\n")
		elif(j == 3):
			frases.append("Busca Best First\n")
		elif(j == 4):
			frases.append("Busca Heurística A\n")
		elif(j == 5):
			frases.append("Busca Heurística A*\n")
		for i in range(n):
			frases.append(str(tamanhosNo[j][i]) + "\t\t\t" + str(tamanhosDist[j][i]) + "\t\t\t" + str(tempos[j][i])+"\n")
	if not os.path.isdir(".//DadosKNN"):
		os.mkdir(".//DadosKNN")
	with open("DadosKNN//Dados" + str(v) + "_" + str(k) + ".txt" , "w") as f:
		f.writelines(frases)

##Função utilizada para comparar os métodos de busca para grafos Random em termos de tempo de execução, comprimento de caminho e número de nós percorridos, podendo realizar a comparação para N exemplos de grafos e tirar a média ao final
def comparaMetodosRand(v , k , n):
	print("V = " , str(v) , " ; K = " , str(k))

	#Inicializando os guardadores de dados para a comparação dos métodos
	tamanhosNo = [[] , [] , [] , [] , [] , []]
	tamanhosDist = [[] , [] , [] , [] , [] , []]
	tempos = [[] , [] , [] , [] , [] , []]
	naoEncontrou = 0

	if not os.path.isdir(".//GraficosRand"):
		os.mkdir(".//GraficosRand")

	#Computando os dados para cada exemplo de grafo
	i = 0
	while (i < n):
		#Gerando o grafo
		nos = grafoRandom(v , k)

		[noInicial, noFinal] = definirNos(nos)
		
		#Computando os dados para cada tipo de busca
		for j in range(6):
			print("i = " , str(i) , " ; j = " , str(j))

			#Realiza a busca
			[caminho, tempo] = iniciarBuscaAuto(noInicial , noFinal , j+1)

			#Caso não exista um caminho entre os nós, cancela esse grafo e gera outro
			if (caminho == None):
				naoEncontrou += 1
				i -= 1
				break

			#Guarda os dados calculados
			tamanhosNo[j].append(len(caminho))
			tamanhosDist[j].append(calcularComprimento(caminho))
			tempos[j].append(tempo)

			#Salva imagens do primeiro exemplo de grafo gerado, com os caminhos encontrados por cada método desenhados
			if (i == 0):
				plotGrafo(nos, False)
				plotCaminho(caminho)
				if(j == 0):
					plt.suptitle("Busca em Profundidade")
					if not os.path.isdir(".//GraficosRand//Profundidade//"):
						os.mkdir(".//GraficosRand//Profundidade//")
					plt.savefig("GraficosRand//Profundidade//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 1):
					plt.suptitle("Busca em Largura por pontos")
					if not os.path.isdir(".//GraficosRand//LarguraNo//"):
						os.mkdir(".//GraficosRand//LarguraNo//")
					plt.savefig("GraficosRand//LarguraNo//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 2):
					plt.suptitle("Busca em Largura por distância")
					if not os.path.isdir(".//GraficosRand//LarguraDist//"):
						os.mkdir(".//GraficosRand//LarguraDist//")
					plt.savefig("GraficosRand//LarguraDist//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 3):
					plt.suptitle("Busca Best First")
					if not os.path.isdir(".//GraficosRand//BestFirst//"):
						os.mkdir(".//GraficosRand//BestFirst//")
					plt.savefig("GraficosRand//BestFirst//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 4):
					plt.suptitle("Busca Heurística A")
					if not os.path.isdir(".//GraficosRand//A//"):
						os.mkdir(".//GraficosRand//A//")
					plt.savefig("GraficosRand//A//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				elif(j == 5):
					plt.suptitle("Busca Heurística A*")
					if not os.path.isdir(".//GraficosRand//AEstrela//"):
						os.mkdir(".//GraficosRand//AEstrela//")
					plt.savefig("GraficosRand//AEstrela//Grafico" + "_" + str(v) + "_" + str(k) + ".png")
				plt.close()
		i += 1

	#Salva os dados computados em um arquivo de texto
	frases = []
	frases.append("Número de vezes que não foi encontrado caminho: " + str(naoEncontrou) + "\n")
	frases.append("\n")
	frases.append("Número de Nós Percorridos\t\tComprimento do Caminho\t\tTempo de Execução\n")
	for j in range(6):
		frases.append("\n")
		if(j == 0):
			frases.append("Busca em Profundidade\n")
		elif(j == 1):
			frases.append("Busca em Largura por pontos\n")
		elif(j == 2):
			frases.append("Busca em Largura por distância\n")
		elif(j == 3):
			frases.append("Busca Best First\n")
		elif(j == 4):
			frases.append("Busca Heurística A\n")
		elif(j == 5):
			frases.append("Busca Heurística A*\n")
		for i in range(n):
			frases.append(str(tamanhosNo[j][i]) + "\t\t\t" + str(tamanhosDist[j][i]) + "\t\t\t" + str(tempos[j][i])+ "\n")
	if not os.path.isdir(".//DadosRand//"):
		os.mkdir(".//DadosRand//")
	with open("DadosRand//Dados" + "_" + str(v) + "_" + str(k) + ".txt" , "w") as f:
		f.writelines(frases)


#testaMetodos()