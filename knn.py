#-*- coding: utf8 -*-
import csv, random, math, operator

def carregarDados(arquivo,split,listaTreino=[],listaTeste=[]):
	
	with open(arquivo,'rb') as arquivoCSV:
		linhas = csv.reader(arquivoCSV)
		dados = list(linhas)
		for x in range(len(dados)-1):
			for y in range(4):
				dados[x][y] = float(dados[x][y])
			if random.random() < split:
				listaTreino.append(dados[x])
			else:
				listaTeste.append(dados[x])

def distanciaEuclidiana(instancia1, instancia2, comp):
	distancia = 0
	for x in range(comp):
		distancia += pow((instancia1[x]-instancia2[x]),2)
	return math.sqrt(distancia)

def selecionaVizinhos(listaTreino, instanciaTeste, k):
	distancias = []
	comp = len(instanciaTeste)-1
	for x in range(len(listaTreino)):
		dist = distanciaEuclidiana(instanciaTeste,listaTreino[x],comp)
		distancias.append((listaTreino[x],dist))
	distancias.sort(key=operator.itemgetter(1))
	vizinhos = []
	for x in range(k):
		vizinhos.append(distancias[x][0])
	return vizinhos

def classificar(vizinhos):
	votos = {}
	for x in range(len(vizinhos)):
		resultado = vizinhos[x][-1]
		if resultado in votos:
			votos[resultado] += 1
		else:
			votos[resultado] = 1
	votosOrdenados = sorted(votos.iteritems(),key=operator.itemgetter(1),reverse=True)
	return votosOrdenados[0][0]

def calcPrecisao(listaTeste,previsoes):
	correto = 0
	for x in range(len(listaTeste)):
		if listaTeste[x][-1] == previsoes[x]:
			correto += 1
	return (correto/float(len(listaTeste))) * 100.0

def knn():
	listaTreino = []
	listaTeste = []
	split = 0.70
	carregarDados('iris.data',split,listaTreino,listaTeste)
	print 'casos de treino: ' + repr(len(listaTreino))
	print 'casos de teste: ' + repr(len(listaTeste))
	previsoes = []
	k = 3
	for x in range(len(listaTeste)):
		vizinhos = selecionaVizinhos(listaTreino,listaTeste[x],k)
		resultado = classificar(vizinhos)
		previsoes.append(resultado)
		print 'classificação = ' + repr(resultado) + ' /-/  atual = ' + repr(listaTeste[x][-1])
	precisao = calcPrecisao(listaTeste,previsoes)
	print 'Precisão: ' + repr(precisao) + '%'

knn()