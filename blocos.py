import pygame
from configuracoes import Blocos_Dados

BLACK = (0, 0, 0)

class Blocos(pygame.sprite.Sprite):
    def __init__(self, cor=Blocos_Dados.cor, largura=Blocos_Dados.tamanhoX-Blocos_Dados.margem, altura=Blocos_Dados.tamanhoY-Blocos_Dados.margem):
        #Chama o construtor da classe pai (Sprite)
        super().__init__()

        self.image = pygame.Surface([largura, altura])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, cor, [0, 0, largura, altura])

        self.rect = self.image.get_rect()