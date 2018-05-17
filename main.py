import sys

Simbolo = 0
Epsilon = 1 #Representado con un &
Vacio = 2 #Representado con un %
ParenAbre = 3
ParenCierra = 4
ClausuraT = 5
ClausuraP = 6
Union = 7 #Representado con un /
Final = 8

# Contador de estados
Contador = 0

# Una TAS mediante un diccionario
# El diccionario es un tipo de dato donde hay claves (no modificables) y valores para esas claves.
TAS = {
	Simbolo: {
		"S": ["T","X"],
		"T": ["R","Z"],
		"Z": ["R","Z"],
		"R": ["M","J"],
		"J": ["&"],
		"M": [Simbolo]
	},
	Epsilon: {	
		"S": ["T","X"],
		"T": ["R","Z"],
		"Z": ["R","Z"],
		"R": ["M","J"],
		"J": ["&"],
		"M": [Epsilon]
	},
	Vacio: {
		"S": ["T","X"],
		"T": ["R","Z"],
		"Z": ["R","Z"],
		"R": ["M","J"],
		"J": ["&"],
		"M": [Vacio]
	},
	ParenAbre: {
		"S": ["T","X"],
		"T": ["R","Z"],
		"Z": ["R","Z"],
		"R": ["M","J"],
		"J": ["&"],
		"M": [ParenAbre,"S",ParenCierra]
	},
	ParenCierra: {
		"X": ["&"],
		"Z": ["&"],
		"J": ["&"]
	},
	ClausuraT: {
		"J": [ClausuraT,"J"]
	},
	ClausuraP: {
		"J": [ClausuraP,"J"]
	},
	Union: {
		"X": [Union,"T","X"],
		"Z": ["&"],
		"J": ["&"]
	},
	Final: {
		"X": ["&"],
		"Z": ["&"],
		"J": ["&"]
	}
}

# Conjunto de Terminales, Conjunto de Variables
Terminales = [Simbolo,Epsilon,ParenAbre,ParenCierra,Union,ClausuraT,ClausuraP,Vacio,Final]
Variables = ["S","X","T","Z","R","J","M"]

# Clase contador:
# class Contador:
# 	def __init__(self):
# 		self.cont = 0

# 	def get_contador(self):
# 		return self.cont

# 	def add_to_contador(self,num):
# 		self.cont = self.cont + num

# Clase para representacion del Arbol
class Nodo:
	def __init__(self,dato,padre):
		self.dato = dato
		self.padre = padre
		self.hijos = []

	def agregar_hijo(self,hijo):
		self.hijos.append(hijo)

	def get_padre(self):
		return self.padre

	def get_hijos(self):
		return self.hijos

	def get_dato(self):
		return self.dato

# Clase de pila, apilar para agregar elemento al top de la pila, desapilar para eliminar el elemento al top de la pila
class Pila:
	def __init__(self):
		self.pila = []

	def apilar(self,simbolo):
		self.pila.append(simbolo)

	def desapilar(self):
		return self.pila.pop()

	def mostrar_pila(self):
		print(self.pila)

# Clase AFD:
class AFD:
	def __init__(self,conjEstados,alfabeto,estadoInicial,estadoFinal,funcTransicion):
		self.conjEstados = conjEstados
		self.alfabeto = alfabeto
		self.estadoInicial = estadoInicial
		self.estadoFinal = estadoFinal
		self.funcTransicion = funcTransicion

	def get_estados(self):
		return self.conjEstados

	def get_alfabeto(self):
		return self.alfabeto

	def get_estado_inicial(self):
		return self.estadoInicial

	def get_estado_final(self):
		return self.estadoFinal

	def get_func_transicion(self):
		return self.funcTransicion

	def minimizar(self):
		particiones = [self.estadoFinal, list(set(self.conjEstados).difference(self.estadoFinal))]
		aux = []
		while particiones != aux:
			if aux != []:
				particiones = list(aux)
			aux = []
			for part in particiones:
				for estado in part:
					tmp = []
					funcTrans = {}
					for simb in self.alfabeto:
						funcTrans[simb] = self.get_indice_grupo(particiones,self.funcTransicion[estado][simb])
					for estado2 in part:
						igualTrans = True
						if estado2 != estado:
							for simb in self.alfabeto:
								if funcTrans[simb] != self.get_indice_grupo(particiones,self.funcTransicion[estado2][simb]):
									igualTrans = False
						if igualTrans:
							tmp.append(estado2)
					if sorted(tmp) not in aux:
						aux.append(sorted(tmp))
		funcTrans = {}
		conjEstados = []
		estadoInicial = None
		estadoFinal = []
		#Armo la funcion de transicion y el conjunto de estados
		for part in particiones:
			if estadoInicial == None:
				if self.estadoInicial in part:
					estadoInicial = particiones.index(part)
			for estF in self.estadoFinal:
				if estF in part and particiones.index(part) not in estadoFinal:
					estadoFinal.append(particiones.index(part))

			for simb in self.alfabeto:
				if particiones.index(part) not in funcTrans:
					funcTrans[particiones.index(part)] = {}
				funcTrans[particiones.index(part)].update({simb: self.get_indice_grupo(particiones,self.funcTransicion[part[0]][simb])})
			conjEstados.append(particiones.index(part))
		self.funcTransicion = funcTrans
		self.conjEstados = conjEstados
		self.estadoInicial = estadoInicial
		self.estadoFinal = estadoFinal

	def get_indice_grupo(self, particiones, estado):
		for part in particiones:
			if estado in part:
				return particiones.index(part)


# Clase AFND:
class AFND:
	def __init__(self,conjEstados, alfabeto, estadoInicial,estadoFinal,funcionTransicion):
		self.conjEstados = conjEstados
		self.alfabeto = alfabeto
		self.estadoInicial = estadoInicial
		self.estadoFinal = estadoFinal
		self.funcTransicion = funcionTransicion

	def get_estados(self):
		return self.conjEstados

	def get_alfabeto(self):
		return self.alfabeto

	def get_estado_inicial(self):
		return self.estadoInicial

	def get_estado_final(self):
		return self.estadoFinal

	def get_funcion_transicion(self):
		return self.funcTransicion

	def eclausura(self,T):
		resultado = []
		for s in T:
			if s != None:
				if s not in resultado:
					resultado.append(s)
				if "&" in self.funcTransicion[s]:
					subs = self.eclausura(self.funcTransicion[s]["&"])
					for estado in subs:
						if estado not in resultado:
							resultado.append(estado)
		return resultado

	def mueve(self,T,a):
		resultado = []
		for s in T:
			if a in self.funcTransicion[s]:
				for estado in self.funcTransicion[s][a]:
					if estado not in resultado and estado !=None:
						resultado.append(estado)
		return resultado

	def transformarAFD(self):
		global Contador
		alfabeto = list(self.alfabeto)
		if "&" in self.alfabeto:
			alfabeto.remove("&")
		conjEstados = [Contador]
		estadoInicial = Contador
		estadoFinal = []
		estados = {
			Contador: sorted(self.eclausura([self.estadoInicial]))
		}
		if set(self.estadoFinal).intersection(self.eclausura([self.estadoInicial])):
			estadoFinal.append(Contador)
		notratados = [Contador]
		Contador += 1
		funcTransicion = {}
		aux = estados.copy()
		while notratados:
			for estado in estados:
				if estado in notratados:
					notratados.remove(estado)
					for simb in alfabeto:
						res = sorted(self.eclausura(self.mueve(estados[estado],simb)))
						if res in aux.values():
							for est in aux:
								if aux[est] == res:
									if estado not in funcTransicion:
										funcTransicion[estado] ={}
									funcTransicion[estado].update({simb:est})
						else:
							aux[Contador] = res
							conjEstados.append(Contador)
							if set(self.estadoFinal).intersection(res):
								estadoFinal.append(Contador)
							notratados.append(Contador)
							if estado not in funcTransicion:
								funcTransicion[estado] ={}
							funcTransicion[estado].update({simb: Contador})
							Contador +=1
			estados = aux.copy()
		return AFD(conjEstados,alfabeto,estadoInicial,estadoFinal,funcTransicion)

	def concatenar(self,afnd):	
		for simbolo in afnd.get_alfabeto():
			if simbolo not in self.alfabeto:
				self.alfabeto.append(simbolo)
		if "&" not in self.alfabeto:
			self.alfabeto.append("&")
		for estado in afnd.get_estados():
			self.conjEstados.append(estado)
		for efinal in self.estadoFinal:
			self.funcTransicion[efinal] = {"&": [afnd.get_estado_inicial()]}
		self.funcTransicion.update(afnd.get_funcion_transicion())
		self.estadoFinal = afnd.get_estado_final()

	def unir(self,afnd):
		global Contador
		for simbolo in afnd.get_alfabeto():
			if simbolo not in self.alfabeto:
				self.alfabeto.append(simbolo)
		for estado in afnd.get_estados():
			self.conjEstados.append(estado)
		if "&" not in self.alfabeto:
			self.alfabeto.append("&")
		self.funcTransicion.update(afnd.get_funcion_transicion())
		self.funcTransicion[Contador] = {"&": [self.estadoInicial,afnd.get_estado_inicial()]}
		self.funcTransicion[Contador+1] = {}
		for efinal in self.estadoFinal:
			self.funcTransicion[efinal]["&"] = [Contador+1]
		for efinal in afnd.get_estado_final():
			self.funcTransicion[efinal]["&"] = [Contador+1]
		self.conjEstados += [Contador, Contador+1]
		self.estadoInicial = Contador
		self.estadoFinal = [Contador + 1]
		Contador = Contador + 2

	def clausurarTran(self):
		global Contador
		if "&" not in self.alfabeto:
			self.alfabeto.append("&")
		for efinal in self.estadoFinal:
			self.funcTransicion[efinal] = {"&": [self.estadoInicial,Contador+1]}
		self.funcTransicion[Contador] = {"&": [self.estadoInicial,Contador+1]}
		self.funcTransicion[Contador+1] = {}
		self.conjEstados += [Contador, Contador+1]
		self.estadoInicial = Contador
		self.estadoFinal = [Contador + 1]
		Contador = Contador + 2

	def clausuraPos(self):
		global Contador
		if "&" not in self.alfabeto:
			self.alfabeto.append("&")
		for efinal in self.estadoFinal:
			self.funcTransicion[efinal] = {"&": [self.estadoInicial,Contador+1]}
		self.funcTransicion[Contador] = {"&": [self.estadoInicial]}
		self.funcTransicion[Contador+1] = {}
		self.conjEstados += [Contador,Contador+1]
		self.estadoInicial = Contador
		self.estadoFinal = [Contador + 1]
		Contador = Contador + 2



# Clase evaluador - Genera los AFND correspondiente a cada produccion, simbolo, etc
class Evaluador:
	def __init__(self,arbol):
		self.resultado = self.evaluarS(arbol)

	def devolver(self):
		return self.resultado

	def evaluarS(self,arbol):
		hijos = arbol.get_hijos()
		afne1 = self.evaluarT(hijos[0])
		return self.evaluarX(hijos[1],afne1)

	def evaluarT(self,arbol):
		hijos = arbol.get_hijos()
		afne1 = self.evaluarR(hijos[0])
		return self.evaluarZ(hijos[1],afne1)

	def evaluarX(self,arbol,afne):
		hijos = arbol.get_hijos()
		if hijos[0].get_dato() == "&":
			return afne
		else:
			afne1 = self.evaluarT(hijos[1])
			afne.unir(afne1)
			return self.evaluarX(hijos[2],afne)

	def evaluarR(self,arbol):
		hijos = arbol.get_hijos()
		afne1 = self.evaluarM(hijos[0])
		return self.evaluarJ(hijos[1],afne1)

	def evaluarZ(self,arbol,afne):
		hijos = arbol.get_hijos()
		if hijos[0].get_dato() == "&":
			return afne
		else:
			afne1 = self.evaluarR(hijos[0])
			afne.concatenar(afne1)
			return self.evaluarZ(hijos[1],afne)

	def evaluarM(self,arbol):
		hijos = arbol.get_hijos()
		if hijos[0].get_dato() == Simbolo:
			return self.evaluarSimb(hijos[0])
		elif hijos[0].get_dato() == Vacio:
			return self.evaluarVacio()
		elif hijos[0].get_dato() == ParenAbre:
			return self.evaluarS(hijos[1])
		elif hijos[0].get_dato() == Epsilon:
			return self.evaluarEpsilon()

	def evaluarJ(self,arbol,afne):
		hijos = arbol.get_hijos()
		if hijos[0].get_dato() == "&":
			return afne
		elif hijos[0].get_dato() == ClausuraT:
			afne.clausurarTran()
			return self.evaluarJ(hijos[1],afne)
		elif hijos[0].get_dato() == ClausuraP:
			afne.clausuraPos()
			return self.evaluarJ(hijos[1],afne)

	def evaluarSimb(self,simbolo):
		global Contador
		conjEstados = [Contador, Contador+1]
		simb = simbolo.get_hijos()[0].get_dato()
		alfabeto = [simb]
		estInicial = Contador
		estFinal = [Contador + 1]
		funcTrans = {
			Contador: {
				simb: [Contador+1]
			},
			Contador+1: {
				simb: [None]
			}
		}
		Contador = Contador + 2
		return AFND(conjEstados,alfabeto,estInicial,estFinal,funcTrans)

	def evaluarVacio(self):
		global Contador
		conjEstados = [Contador, Contador+1]
		alfabeto = ["%"]
		estInicial = Contador
		estFinal = [Contador + 1]
		funcTrans = {
			Contador: {
				"%": [None]
			},
			Contador+1: {
				"%": [None]
			}
		}
		Contador = Contador + 2
		return AFND(conjEstados,alfabeto,estInicial,estFinal,funcTrans)

	def evaluarEpsilon(self):
		global Contador
		conjEstados = [Contador, Contador+1]
		alfabeto = ["&"]
		estInicial = Contador
		estFinal = [Contador + 1]
		funcTrans = {
			Contador: {
				"&": [Contador+1]
			},
			Contador+1: {
				"&": [None]
			}
		}
		Contador = Contador + 2
		return AFND(conjEstados,alfabeto,estInicial,estFinal,funcTrans)


class AnalizadorSintactico:
	def __init__(self,fuente):
		self.pila = Pila()
		self.pila.apilar(Final)
		self.pila.apilar("S")
		self.raiz = Nodo("S",None)
		self.hojaactual = self.raiz
		self.estado = 0
		self.alexico = AnalizadorLexico(fuente)

	def devolver_arbol(self):
		if self.estado == 2:
			return self.raiz

	def mostrar_arbol(self,nodo):
		if nodo == None:
			pass
		else:
			print(nodo.get_dato())
			for hijo in nodo.get_hijos():
				self.mostrar_arbol(hijo)


	def reconocer(self):
		# Obtiene el primer simbolo de la cadena
		a = self.alexico.obtener_sig_car()
		# Comienza en estado 0 = reconociendo
		# Estado 1 = Error.
		while self.estado == 0:
			# Desapila y obtiene el primer elemento de la pila
			x = self.pila.desapilar()
			# Lista todos los hijos de la hoja actual, si el hijo es igual al elemento en el tope de la pila, nodoactual pasa a ser este
			if x != Final:
				if self.hojaactual.get_hijos():
					for hijo in self.hojaactual.get_hijos():
						if hijo.get_dato() == x:
							self.hojaactual = hijo
				while self.hojaactual.get_dato() != x:
					if self.hojaactual.get_padre() != None:
						self.hojaactual = self.hojaactual.get_padre()
						for hijo in self.hojaactual.get_hijos():
							if hijo.get_dato() == x:
								self.hojaactual = hijo
			# Si x es igual a y ambos son iguales a el Final de la cadena -> Termina el bucle - Avisando que hubo exito
			if x == a[0] ==Final:
				self.estado = 2
			# Si x es un terminal y es igual a -a- obtiene el siguente caracter del analizador lexico. Sino error.
			elif x in Terminales:
				if x != a[0]:
					self.estado = 1
				else:
					self.hojaactual.agregar_hijo(Nodo(a[1],self.hojaactual))
					a = self.alexico.obtener_sig_car()
			# Si x es una variable y esta en la tas mediante el simbolo -a-, apila todos los simbolos de la tas en forma inversa a la pila. Sino error.		
			elif x in Variables:
				if x in TAS[a[0]]:
					# Apila los simbolos de la TAS de forma reversa
					for simb in TAS[a[0]][x][::-1]:
						self.pila.apilar(simb)
					# Arma el arbol con los simbolos de la TAS de forma normal
					for simb in TAS[a[0]][x]:
						self.hojaactual.agregar_hijo(Nodo(simb,self.hojaactual))
				else:
					self.estado = 1
		# Devuelve el estado
		return self.estado
				


class AnalizadorLexico:
	def __init__(self,fuente):
		self.archivo = open(fuente)
		self.simbolo = ""
		self.control = 0
		self.cadena = self.archivo.read()

	def obtener_sig_car(self):
		# Si el len de la cadena es menor o igual al control. La cadena se termino y devuelve un Final
		if len(self.cadena)-1 <= self.control:
			return [Final, "$"]
		# Si no devuelve lo el componente lexico que corresponde al simbolo actual en la cadena. Y avanza la cadena en 1.
		else:
			self.simbolo = self.cadena[self.control]
			while ord(self.simbolo) < 33:
				self.control += 1
				self.simbolo = self.cadena[self.control]
			self.control += 1
			return [self.car_a_simb(self.simbolo), self.simbolo]


	def car_a_simb(self,caracter):
		if caracter == "(":
			return ParenAbre
		elif caracter == ")":
			return ParenCierra
		elif caracter == "*":
			return ClausuraT
		elif caracter == "+":
			return ClausuraP
		elif caracter == "%":
			return Vacio
		elif caracter == "&":
			return Epsilon
		elif caracter == "/":
			return Union
		else:
			return Simbolo

class Proyecto:
	def __init__(self, fuente):
		self.AS = AnalizadorSintactico(fuente)
		self.AS.reconocer()
		self.EV = Evaluador(self.AS.devolver_arbol())
		self.AFND = self.EV.devolver()
		self.AFD = self.AFND.transformarAFD()
		self.AFD.minimizar()

	def mostrar_AFD(self):
		print("Conjunto de Estados: ")
		print(self.AFD.get_estados())
		print("Estado Inicial:")
		print(self.AFD.get_estado_inicial())
		print("Estados Finales:")
		print(self.AFD.get_estado_final())
		print("Funcion de Transicion:")
		print(self.AFD.get_func_transicion())

if __name__ == "__main__":
	Proy = Proyecto(sys.argv[1])
	Proy.mostrar_AFD()
