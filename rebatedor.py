import pygame
from configuracoes import Rebatedor_Dados
from configuracoes import tela

BLACK = (0, 0, 0)

class Rebatedor(pygame.sprite.Sprite):
    def __init__(self, cor=Rebatedor_Dados.cor, largura=Rebatedor_Dados.tamanhoX, altura=Rebatedor_Dados.tamanhoY):
        #Chama o construtor da classe pai (Sprite)
        super().__init__()

        self.image = pygame.Surface([largura, altura])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.velocidade = Rebatedor_Dados.velocidade

        pygame.draw.rect(self.image, cor, [0, 0, largura, altura])

        self.rect = self.image.get_rect()

    def moveLeft(self, y):
        self.rect.x -= y * self.velocidade
        #Verifica se você não está indo muito longe (fora da tela)
        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self, y):
        self.rect.x += y * self.velocidade
        #Verifica se você não está indo muito longe (fora da tela)
        if self.rect.x + Rebatedor_Dados.tamanhoX > tela[0]:
            self.rect.x = tela[0] - Rebatedor_Dados.tamanhoX