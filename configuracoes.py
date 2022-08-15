#Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Tela
tela = (largura, altura) = (600, 600)
FPS = 200
cor = BLACK

#Dados do rebatedor
class Rebatedor_Dados:
    tamanhoX = 80
    tamanhoY = 10
    x = int((largura-tamanhoX)/2)
    y = int(altura-altura/18)
    cor = WHITE
    velocidade = 10

#Dados dos blocos
class Blocos_Dados:
    n_Blocos = 12
    margem = 2
    colunas = 6                       #Linhas(tinha definido errado)
    margemSuperior = 1.2
    tamanhoX = largura/n_Blocos
    tamanhoY = altura/3/colunas - margem
    cor = WHITE

#Dados da bola
class Bola_Dados:
    rad = 10
    centro = [int((largura-rad)/2), int(2*altura/4)]
    cor = WHITE
    velocidade = Rebatedor_Dados.velocidade - 6