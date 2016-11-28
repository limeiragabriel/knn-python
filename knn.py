#-*- coding: utf8 -*-
import csv, random, math, operator

def carregarDados(arquivo,arquivoTeste,listaTreino=[],listaTeste=[]):
	
	with open(arquivo,'rb') as arquivoCSV:
		linhas = csv.reader(arquivoCSV)
		dados = list(linhas)
		for x in range(len(dados)-1):
			for y in range(4):
				dados[x][y] = float(dados[x][y])
			listaTreino.append(dados[x])

	with open(arquivoTeste,'rb') as arquivoCSV2:
		linhas2 = csv.reader(arquivoCSV2)
		dados2 = list(linhas2)
		for x in range(len(dados2)-1):
			for y in range(4):
				dados2[x][y] = float(dados2[x][y])
			listaTeste.append(dados2[x])

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
	carregarDados('iris.data','iris-teste.data',listaTreino,listaTeste)
	print 'casos de treino: ' + repr(len(listaTreino))
	print 'casos de teste: ' + repr(len(listaTeste))
	print '\n resultados: \n'
	previsoes = []
	k = 3
	for x in range(len(listaTeste)):
		vizinhos = selecionaVizinhos(listaTreino,listaTeste[x],k)
		resultado = classificar(vizinhos)
		previsoes.append(resultado)
		print ' ID = ' + repr(listaTeste[x][-1]) + ' ----- classificação = ' + repr(resultado)

knn()