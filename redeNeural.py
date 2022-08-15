#########################################################################################################
#_______________________________Construção da Rede Neural_________________________________________
#########################################################################################################
#Existem 3 ações possíveis:

# 1 - Não fazer nada;
# 2 - Mover para direita;
# 3 - Mover para esquerda;

#Para cada acao desses a rede vai calcular um numero que diz o quao bom e tomar aquela acao naquele momento
#Caso seja ruim ela o erro é aumentado, caso contrario, o erro é zerado.

#Inicio colocando 2 camadas de neuronios na camada de entrada e mais 2 na camada oculta;
#Tambem incluo um neuronio de saida.

import numpy as np
from random import uniform

#Globais
pesosPrimeiroNeuronioCamadaEntrada = np.array([uniform(-1, 1) for i in range(4)])   #Pesos para o primeiro neuronio da camada de entrada
pesosSegundoNeuronioCamadaEntrada = np.array([uniform(-1, 1) for i in range(4)])    #Pesos para o sengundo neuronio da camada de entrada

pesosPrimeiroNeuronioCamadaOculta = np.array([uniform(-1, 1) for i in range(2)])    #Pesos para o primeiro neuronio da camada oculta
pesosSegundoNeuronioCamadaOculta = np.array([uniform(-1, 1) for i in range(2)])     #Pesos para o segundo neuronio da camada oculta

pesosNeuronioDeSaida = np.array([uniform(-1, 1) for i in range(2)])

#Criação da classe
class RedeNeural():
    def __init__(self, XRaquete, XBolinha, YBola, bias = -1):   #Bias definido como -1

        self.entradas = np.array([XRaquete, XBolinha, YBola, bias])     #Entradas referentes ao jogo
        global pesosPrimeiroNeuronioCamadaEntrada, pesosSegundoNeuronioCamadaEntrada, pesosPrimeiroNeuronioCamadaOculta, pesosSegundoNeuronioCamadaOculta

        self.pesosPrimeiroNeuronioCamadaEntrada = pesosPrimeiroNeuronioCamadaEntrada
        self.pesosSegundoNeuronioCamadaEntrada = pesosSegundoNeuronioCamadaEntrada

        self.pesosPrimeiroNeuronioCamadaOculta = pesosPrimeiroNeuronioCamadaOculta
        self.pesosSegundoNeuronioCamadaOculta = pesosSegundoNeuronioCamadaOculta

        self.pesosNeuronioDeSaida = pesosNeuronioDeSaida

    #Faz o somatório da multiplicação das entradas pelo peso e passa pelas funções de ativação
    def feedforward(self):

        self.saidaPrimeiroNeuronioCamadaEntrada = round(self.tangenteHiperbolica(np.sum(self.entradas * self.pesosPrimeiroNeuronioCamadaEntrada)), 6)

        self.saidaSegundoNeuronioCamadaEntrada = round(self.tangenteHiperbolica(np.sum(self.entradas * self.pesosSegundoNeuronioCamadaEntrada)), 6)

        self.saidaPrimeiroNeuronioCamadaOculta = round(self.tangenteHiperbolica(np.sum(np.array([self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaPrimeiroNeuronioCamadaEntrada])  * self.pesosPrimeiroNeuronioCamadaOculta )), 6)

        self.saidaSegundoNeuronioCamadaOculta = round(self.tangenteHiperbolica(
                np.sum(np.array([self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaSegundoNeuronioCamadaEntrada]) * self.saidaSegundoNeuronioCamadaEntrada )), 6)

        self.resultado = round(self.sigmoid(np.sum(np.array([self.saidaPrimeiroNeuronioCamadaOculta, self.saidaSegundoNeuronioCamadaOculta]) * self.pesosNeuronioDeSaida)),6)

        return self.resultado

    #Função de ativação Tangente Hiperbolica
    def tangenteHiperbolica(self, x):
        th = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        return th

    #Função de ativação Sigmoid
    def sigmoid(self, x):
        return 1/ (1 + np.exp(-x))
    
    #Função que faz a atualização dos pesos 
    def atualizaPesos(self, erro, taxaAprendizagem=0.01):

        for i in range(len(pesosNeuronioDeSaida)):
            if i == 0:
                entrada = self.saidaPrimeiroNeuronioCamadaOculta
            elif i == 1:
                entrada = self.saidaSegundoNeuronioCamadaOculta

            pesosNeuronioDeSaida[i] = pesosNeuronioDeSaida[i] + (taxaAprendizagem * entrada * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaOculta)):
            if i == 0:
                entrada1 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada1 = self.saidaSegundoNeuronioCamadaEntrada

            pesosPrimeiroNeuronioCamadaOculta[i] = pesosPrimeiroNeuronioCamadaOculta[i] + (taxaAprendizagem * entrada1 * erro)

        for i in range(len(pesosSegundoNeuronioCamadaOculta)):
            if i == 0:
                entrada2 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada2 = self.saidaSegundoNeuronioCamadaEntrada

            pesosSegundoNeuronioCamadaOculta[i] = pesosSegundoNeuronioCamadaOculta[i] + (taxaAprendizagem * entrada2 * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaEntrada)):
            pesosPrimeiroNeuronioCamadaEntrada[i] = pesosPrimeiroNeuronioCamadaEntrada[i] + (taxaAprendizagem * self.entradas[i] * erro)

        for i in range(len(pesosSegundoNeuronioCamadaEntrada)):
            pesosSegundoNeuronioCamadaEntrada[i] = pesosSegundoNeuronioCamadaEntrada[i] + (taxaAprendizagem * self.entradas[i] * erro)

        #print(self.resultado)
        #Manda os pesos encontrados para um arquivo txt
        #with open('dados.txt', 'w') as arquivo:
        #    arquivo.write("Primeiro neuronio entrada: " + str(pesosPrimeiroNeuronioCamadaEntrada) 
        #                    + "\n" + "Segundo neuronio entrada: " + str(pesosSegundoNeuronioCamadaEntrada) + "\n" 
        #                    + "Primeiro neuronio culta: " + str(pesosPrimeiroNeuronioCamadaOculta) + "\n" 
        #                    + "Segundo neuronio oculta: " + str(pesosSegundoNeuronioCamadaOculta) + "\n" 
        #                    + "Neuronio Saida " + str(self.pesosNeuronioDeSaida) + "\n")