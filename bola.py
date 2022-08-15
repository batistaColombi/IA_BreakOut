from random import randint
import pygame
from configuracoes import Bola_Dados 
from configuracoes import tela

BLACK = (0, 0, 0)

class Bola(pygame.sprite.Sprite):
    def __init__(self, largura, altura, cor=Bola_Dados.cor):
        #Chama o construtor da classe pai (Sprite)
        super().__init__()

        self.image = pygame.Surface([largura, altura])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.ellipse(self.image, cor, [0, 0, largura, altura])

        while True:
            self.movimento = [randint(-1, 1), -1]
            if self.movimento[0] != 0:
                break

        self.velocidade = Bola_Dados.velocidade

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.movimento[0] * self.velocidade
        self.rect.y -= self.movimento[1] * self.velocidade

    def paredes(self):
        #parede esquerda e direita
        if self.rect.x + 2 * Bola_Dados.rad >= tela[0] or self.rect.x <= 0:
            self.movimento[0] *= -1
        #Parede de cima    
        if self.rect.y < 40:
            self.movimento[1] *= -1
        if self.rect.y == 0:
            self.movimento[1] *= -5

    def linha_fundo(self):
        if self.rect.y + 2 * Bola_Dados.rad > tela[1]:
            self.movimento[1] *= -1
            return True