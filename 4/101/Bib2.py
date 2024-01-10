# -*- coding: utf-8 -*-
import math
import os
import subprocess

""" Version: v2.1 """

class Grafo(object):
	"""
	Classe base para as classes GrafoListaAdj e GrafoMatrizAdj
	"""	
	def __init__(self, orientado = False):
		"""
		Grafo se orientado=False ou Digrafo se orientado=True.
		"""
		self.n, self.m, self.d, self.orientado, self.AtrV, self.Subgrafos = None, None, None, orientado, None, None
		
	def DefinirN(self, n, RotulosV = None):
		"""
		Define o número de vértices como n e atribui o rótulo RotulosV[i] para o i-ésimo vértice.
		"""	
		self.n, self.m = n, 0
		self.RotulosV = RotulosV
		self.Rot2V = {}
		if RotulosV != None:
			for i in range(1,len(RotulosV)):
				self.Rot2V[RotulosV[i]] = i
		self.d = [0]*(self.n+1)

	def DefinirSubgrafo(self, SubconjV, Rotulo = None):
		"""
		Define o subgrafo induzido formado pelos vérties em SubconjV, com rótulo Rotulo.
		Subgrafos são levados em conta para o desenho do grafo.
		"""	
		if self.Subgrafos == None:
			self.Subgrafos = []
		self.Subgrafos.append((SubconjV, Rotulo))

	def Ler(self, formato="digitado", textoAuxilio=False):
		"""
		Lê um grafo da entrada padrão.
		Parâmetros:
		    digitado = digitado/graph6
		        (formato 'graph6' necessita ter o nauty instalado no ambiente: http://pallini.di.uniroma1.it/
		         Usuários Ubuntu: 'sudo apt-get install nauty'
		        )
		"""
		if formato=="digitado":
			n = int(input("n = " if textoAuxilio else ""))
			usarRotulo = input("rotular vertices? (S/n) = " if textoAuxilio else "")
			usarRotulo = "S" if usarRotulo == "" else usarRotulo.upper()
			if usarRotulo != "S":
				rotulosV = None
			else:
				rotulosV = [None]
				for i in range(1, n+1):
					rotulosV.append(input("rotulo vertice {0} = ".format(i) if textoAuxilio else ""))
			self.DefinirN(n, rotulosV)

			usarSubgrafos = input("definir subgrafos? (S/n) = " if textoAuxilio else "")
			usarSubgrafos = "S" if usarSubgrafos == "" else usarSubgrafos.upper()
			if usarSubgrafos == "S":
				i = 1
				while True:
					subConjV = input("sequencia 'v1 v2 ...' de vertices do subgrafo #{0} (vazio para terminar) = ".format(i) if textoAuxilio else "").strip()
					if subConjV == "":
						break
					else:
						rotulo = input("rotulo do subgrafo #{0} = ".format(i) if textoAuxilio else "")
						self.DefinirSubgrafo(subConjV.split(), None if rotulo == "" else rotulo)
					i = i+1
		
			self.m = int(input("m = " if textoAuxilio else ""))
			for i in range(self.m):
				u = input("aresta #{0} (u, v): u = ".format(i+1) if textoAuxilio else "")
				v = input("aresta #{0} (u, v): v = ".format(i+1) if textoAuxilio else "")
				try:
					u, v = int(u), int(v)
				except:
					u, v = u, v
				self.AdicionarAresta(u, v)
				u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
				self.d[u] += 1
				self.d[v] += 1

		elif formato=="graph6":
			grafo = input("cadeia que representa o grafo no formato graph6 = " if textoAuxilio else "")
			linhas = subprocess.Popen(["showg", "-a"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate("{0}\n".format(grafo))[0].split("\n")
			linhas = linhas[2:len(linhas)-1]
			self.DefinirN(len(linhas))
			u = 1
			for linha in linhas:
				for v in range(u+1, self.n+1):
					if linha[v-1] == "1":
						self.AdicionarAresta(u, v)
						self.d[u] += 1
						self.d[v] += 1
				u = u+1
									
	def ObterRotuloV(self, v):
		"""
		Retorna o rótulo do vértice v.
		"""	
		if self.RotulosV == None or self.RotulosV[v] == None:
			return ""
		else:
			return self.RotulosV[v] 

	def ObterVdeRotulo(self, rotulo):
		"""
		Retorna o vértice com o dado rótulo.
		"""	
		if self.RotulosV == None or not isinstance(rotulo, str):
			return rotulo
		else:
			return self.Rot2V[rotulo] 

	def ObterAtrV(self, v):
		"""
		Retorna os atributos do vértice v.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		if self.AtrV == None or self.AtrV[v] == None:
			return ""
		else:
			return self.AtrV[v] 
			
	def DefinirAtrV(self, v, atr):
		"""
		Define os atributos atr do vértice v. Exemplo: atr='fillcolor=yellow shape=box'.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		if self.AtrV == None:
			self.AtrV = [None]*(self.n+1)
		self.AtrV[v] = atr
	
	def V(self):
		"""
		Retorna lista de vértices.
		"""
		for i in range(1,self.n+1):
			yield i
	def E(self):
		"""
		Retorna lista de arestas uv, onde u é um inteiro e v é um inteiro se o grafo é GrafoMatrizAdj
		ou v é GrafoListaAdj.NoAresta, caso contrário.
		"""
		for v in self.V():
			for viz in self.N(v, Tipo = "+" if self.orientado else "*"):
				enumerar = True
				if not self.orientado:
					vizint = viz if isinstance(viz, int) else viz.Viz
					enumerar = v < vizint
				if enumerar:
					yield (v, viz)
	#def AdicionarVertice():
	#	raise Exception("not supported!")

	#def RemoverAresta(u, v):
	#	raise Exception("not supported!")

	#def Induzido(V):
	#	raise Exception("not supported!")

	#def Uniao(G):
	#	raise Exception("not supported!")

		
	def Desenhar(self, arquivoSaida="graph.png", engine="default", reduzirTempo=False):
		"""
		Gera o desenho do grafo no arquivo arquivoSaida usando algoritmo de layout indicado em engine. Se o grafo 
		for muito grande, o tempo de resposta pode ser longo se reduzirTempo=False. Para obter layouts mais rápidos
		de serem produzidos (em detrimento da qualidade), utilize reduzirTempo=True.
		Para a geração do arquivo de imagem, é necessário ter o GraphViz instalado no ambiente: http://www.graphviz.org
		Usuários Ubuntu: 'sudo apt-get install graphviz'
		"""
		arquivoSaida = os.path.expanduser(arquivoSaida)
		arquivoEntrada = arquivoSaida + ".dot"
		f = open(arquivoEntrada, "w")
		if self.orientado:
			f.write("digraph {\n");
			edge = "->"
		else:
			f.write("graph {\n");
			edge = "--"
		Poverlap = "scale" if reduzirTempo else "false"
		Psplines = "curved" if reduzirTempo else "true"
		
		f.write("    graph [splines={1} overlap={0}];\n".format(Poverlap, Psplines))
		f.write("    node [shape=circle style=filled];\n".format(Poverlap, Psplines))

		f.write("    ");
		for u in range(1, self.n+1):
			r = self.ObterRotuloV(u)
			r = "" if r == "" else "label=\"{0}\"".format(r)
			r = (r + " " + self.ObterAtrV(u)).strip()
			r = "" if r == "" else " [{0}]".format(r)
			f.write(str(u) + r + " ")
		f.write(";\n");
		
		if self.Subgrafos != None:
			i = 1
			for (subconjv, rotulo) in self.Subgrafos:
				#print (subconjv, rotulo)
				f.write("    subgraph cluster_" + str(i) + " {")
				f.write("color=blue; ")
				if rotulo != None:
					f.write("label=\"{0}\"".format(rotulo) + "; ")
				for u in subconjv:
					f.write(str(u) + " ")
				f.write(";}\n");
				i = i+1
					
		for u in range(1, self.n+1):
			for v in self.N(u, "+" if self.orientado else "*", IterarSobreNo=True):
				if not isinstance(v, int):
					r = self.ObterAtrE(v)
					v = v.Viz
				else:
					r = self.ObterAtrE(u,v)
				r = "" if r == "" else " [{0}]".format(r)
				if self.orientado or u < v:				
					f.write(str(u) + edge + str(v) + r + ";\n")
		f.write("}")
		f.close()
		if engine=="default" and self.n <= 150:
			engine = "dot"
		else:
			engine = "sfdp"
		
		if engine == "dot":
			os.system("dot -Tpng " + arquivoEntrada + " -o " + arquivoSaida)
		else:
			os.system("sfdp -Tpng " + arquivoEntrada + " -o " + arquivoSaida)
		

class GrafoMatrizAdj(Grafo):

	def DefinirN(self, n, RotulosV = None):
		"""
		Define o número de vértices como n e atribui o rótulo RotulosV[i] para o i-ésimo vértice.
		"""	
		super(GrafoMatrizAdj, self).DefinirN(n, RotulosV)
		self.M = [None]*(self.n+1)
		self.AtrE, self.AtrV = None, None
		
		for i in range(1, self.n+1):
			self.M[i] = [0]*(int(math.ceil(self.n/32.0))+1)

	def ObterAtrE(self, u, v):
		"""
		Retorna os atributos da aresta uv.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		if self.AtrE == None or self.AtrE[u][v] == None:
			return ""
		else:
			return self.AtrE[u][v]
			
	def DefinirAtrE(self, u, v, atr):
		"""
		Define os atributos atr da aresta uv. Exemplo: atr='fillcolor=yellow shape=box'.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		if self.AtrE == None:
			self.AtrE = [None]*(self.n+1)
			for i in range(1, self.n+1):
				self.AtrE[i] = [None]*(self.n+1)
		self.AtrE[u][v] = atr
		if not self.orientado:
			self.AtrE[v][u] = atr
			
	def AdicionarAresta(self, u, v, atr=""):
		"""
		Adiciona aresta uv com atributo atr ao grafo. Exemplo, atr='label="abc" color=blue'.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		l, c = u, (v-1) // 32 + 1
		p = v - 32*(c-1)
		self.M[l][c] = self.M[l][c] | (1 << (p-1))
		if not self.orientado:
			u, v = v, u
			l, c = u, (v-1) // 32 + 1
			p = v - 32*(c-1)
			self.M[l][c] = self.M[l][c] | (1 << (p-1))
		if atr != "":
			self.DefinirAtrE(u, v, atr)
		self.m = self.m+1		
			
	def EhAresta(self, u, v):
		"""
		Retorna True se uv é uma aresta e False, caso contrário.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		l, c = u, (v-1) // 32 + 1
		p = v - 32*(c-1)
		return (self.M[l][c] & (1 << (p-1))) > 0

	def N(self, v, Tipo = "*", Fechada=False, IterarSobreNo=False):
		"""
		Retorna lista de vértices vizinhos do vértice v. Se Fechada=True, o próprio v é incluido na lista.
		Tipo="*" significa listar todas as arestas incidentes em v. Se G é orientado, 
		Tipo="+" (resp. "-") significa listar apenas as arestas de saída (resp. entrada) de v.
		IterarSobreNo não tem uso para Matriz de Adjacências.
		"""
		if Fechada:
			yield v
		w = 1
		t = "+" if Tipo == "*" and self.orientado else Tipo
		while w <= self.n:
			if t == "+":
				orig, dest, viz = v, w, w
			else:
				orig, dest, viz = w, v, w
			if self.EhAresta(orig, dest):
				yield w
			w = w+1
			if w > self.n and t == "+" and Tipo == "*":
				t, w = "-", 1
			


class GrafoListaAdj(Grafo):
	class NoAresta(object):
		"""
		Objeto nó da lista de adjacência.
		Atributos:
		- Viz (vizinho)
		- e (Aresta)
		- Prox (próxima aresta na lista de adjacência)
		"""	

		def __init__(self):
			self.Viz = None
			self.e = None
			self.Prox = None

	class Aresta(object):
		"""
		Objeto único para representar a aresta.
		Atributos:
		- v1 (um dos vértices desta aresta)
		- v2 (o outro vértice desta aresta)
		- atr (atributos)
		"""
		def __init__(self):
			self.v1 = None
			self.v2 = None
			self.atr = None

	def DefinirN(self, n, RotulosV = None):
		"""
		Define o número de vértices como n e atribui o rótulo RotulosV[i] para o i-ésimo vértice.
		"""	
		super(GrafoListaAdj, self).DefinirN(n, RotulosV)
		self.L = [None]*(self.n+1)

	def ObterAtrE(self, uv):
		"""
		Retorna os atributos da aresta uv.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		if isinstance(uv, GrafoListaAdj.NoAresta):
			uv = uv.e
		return "" if uv.atr == None else uv.atr
			
	def DefinirAtrE(self, uv, atr):
		"""
		Define os atributos atr da aresta uv. Exemplo: atr='fillcolor=yellow shape=box'.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		if isinstance(uv, GrafoListaAdj.NoAresta):
			uv = uv.e
		uv.atr = atr
				
	def AdicionarAresta(self, u, v, atr = ""):
		"""
		Adiciona aresta uv com atributo atr ao grafo. Exemplo, atr='label="abc" color=blue'.
		Para lista completa de atributos possívels, consulte http://www.graphviz.org/doc/info/attrs.html.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		
		e = GrafoListaAdj.Aresta()
		e.v1, e.v2 = u, v
		No = GrafoListaAdj.NoAresta()
		No.Viz, No.e, No.Prox, self.L[u] = v, e, self.L[u], No
		if self.orientado:
			No.Tipo = "+"
		No = GrafoListaAdj.NoAresta()
		No.Viz, No.e, No.Prox, self.L[v] = u, e, self.L[v], No
		if self.orientado:
			No.Tipo = "-"
		if atr != "":
			self.DefinirAtrE(No, atr)
		self.m = self.m+1
		return e
		
	def EhAresta(self, u, v):
		"""
		Retorna True se uv é uma aresta e False, caso contrário.
		"""
		u, v = self.ObterVdeRotulo(u), self.ObterVdeRotulo(v)
		Tipo = "+" if self.orientado else "*"
		for w in self.N(u, Tipo):
			if w == v:
				return True
		return False

	def N(self, v, Tipo = "*", Fechada=False, IterarSobreNo=False):
		"""
		Retorna lista de Grafo.NoAresta representando os vizinhos do vértice v. 
		Se Fechada=True, o próprio v é incluido na lista.
		Tipo="*" significa listar todas as arestas incidentes em v. Se G é orientado, 
		Tipo="+" (resp. "-") significa listar apenas as arestas de saída (resp. entrada) de v.
		IterarSobreNo=False indica que a lista de vizinhos constitue-se da lista de vértices (inteiros). Caso
		contrário, a lista é de NoAresta.
		"""
		if Fechada:
			No = GrafoListaAdj.NoAresta()
			No.Viz, No.e, No.Prox = v, None, None
			yield No if IterarSobreNo else No.Viz
		w = self.L[v]
		while w != None:
			if Tipo == "*" or w.Tipo == Tipo:
				yield w if IterarSobreNo else w.Viz
			w = w.Prox
			
			
			
			
			
