from cmath import nan
import sys
import pygame
from rebatedor import Rebatedor
from bola import Bola
from blocos import Blocos

from redeNeural import RedeNeural
from configuracoes import (tela, FPS, cor, Rebatedor_Dados, Bola_Dados, Blocos_Dados)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

vidas = 100
atualizacao = 1
pontos = [0]
contador = 0

def start(telaJogo, i, j):
    startMargem = 18

def game(live):
    pygame.init()

    #tela
    telaJogo = pygame.display.set_mode(tela) #cria tela
    pygame.display.set_caption('IA_Breakout')
    clock = pygame.time.Clock()

    all_sprites_list = pygame.sprite.Group()

    lives = live
    fimJogo = False

    telaJogo.fill(cor)

    #Cria rebatedor
    rebatedor = Rebatedor()
    rebatedor.rect.x = Rebatedor_Dados.x
    rebatedor.rect.y = Rebatedor_Dados.y

    #Cria bola
    bola = Bola(2*Bola_Dados.rad, 2*Bola_Dados.rad)
    bola.rect.x = Bola_Dados.centro[0] - Bola_Dados.rad
    bola.rect.y = Bola_Dados.centro[1] - Bola_Dados.rad

    #Cria blocos
    todosBlocos = pygame.sprite.Group()
    for y in range(Blocos_Dados.colunas):
        for x in range(0, tela[0], int(Blocos_Dados.tamanhoX)):
            blocos = Blocos()
            blocos.rect.x = x + Blocos_Dados.margem
            blocos.rect.y = int(Blocos_Dados.tamanhoY) * (y + Blocos_Dados.margemSuperior) + Blocos_Dados.margem
            all_sprites_list.add(blocos)
            todosBlocos.add(blocos)

    all_sprites_list.add(rebatedor)
    all_sprites_list.add(bola)

    while not fimJogo:
        global vidas, atualizacao, contador

        #Rede__________________________________________________________________________________________________
        rede = RedeNeural(rebatedor.rect.x/600, bola.rect.x/600, bola.rect.y/600)
        tecla = rede.feedforward()

        #Manipula entrada do IA
        for event in pygame.event.get(): #obtem eventos como pressionamento de tecla, clique do mouse, etc
            if event.type == pygame.QUIT:
                fimJogo = True

        #Move rebatedor_____________________________________________________________________________________    
        if tecla < 0.5 and tecla > 0.2:
            rebatedor.moveLeft(1) 

        if tecla < 0.2 and tecla >= 0:
            erro = ((rebatedor.rect.x) - (bola.rect.x)) /100 #Calcula e atualiza erro
            rede.atualizaPesos(erro)

            rebatedor.moveRight(1) 

        if tecla > 0.5 and tecla < 0.8:
            rebatedor.moveRight(1)
        
        if tecla > 0.8 and tecla <= 1:
            erro = ((rebatedor.rect.x) - (bola.rect.x)) /100 #Calcula e atualiza erro
            rede.atualizaPesos(erro)

            rebatedor.moveLeft(1)

        if tecla == nan:
            pygame.quit() #Sai pygame
            sys.exit() #Deixa programa)

        #Verifica paredes__________________________________________________________________________________________________
        
        bola.paredes()

        if bola.linha_fundo():
            vidas -= 1
            pontos[0] -= 5
            contador += 1

            erro = ((rebatedor.rect.x) - (bola.rect.x)) /100    #Calcula e atualiza erro
            rede.atualizaPesos(erro)

            with open('dadosTreinamento.txt', 'a') as arquivo:
                    arquivo.write('atualizacao: ' + str(atualizacao) +' '+ 'Erro: ' + str(erro) + "\n")

            if contador == 10:
                pontos[0] = 0
                contador = 0
                atualizacao += 1

                erro = ((rebatedor.rect.x) - (bola.rect.x)) /10 #Calcula e atualiza erro
                rede.atualizaPesos(erro) 

                #Desenha
                telaJogo.fill(cor)

                #Pontuacao
                font = pygame.font.Font(None, 40)
                text = font.render('Pontos: ',1, WHITE)
                telaJogo.blit(text, (20, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(pontos[0]), 1, WHITE)
                telaJogo.blit(text, (130, 7))

                #vidas(contador)
                font = pygame.font.Font(None, 40)
                text = font.render('Mortes: ',1, WHITE)
                telaJogo.blit(text, (220, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(contador), 1, WHITE)
                telaJogo.blit(text, (330, 7))

                #atualizacao
                font = pygame.font.Font(None, 40)
                text = font.render('Atualizacao: ',1, WHITE)
                telaJogo.blit(text, (380, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(atualizacao), 1, WHITE)
                telaJogo.blit(text, (560, 7))

                #Todos os sprites
                all_sprites_list.draw(telaJogo)
                pygame.draw.line(telaJogo, WHITE, [0, 35], [800, 35], 2)

                pygame.display.flip()
                clock.tick(FPS)
 
            #Desenha
            telaJogo.fill(cor)

            #Pontuacao
            font = pygame.font.Font(None, 40)
            text = font.render('Pontos:', 1, WHITE)
            telaJogo.blit(text, (20, 7))

            font = pygame.font.Font(None, 40)
            text = font.render(str(pontos[0]), 1, WHITE)
            telaJogo.blit(text, (130, 7))

            #vidas(contador)
            font = pygame.font.Font(None, 40)
            text = font.render('Mortes: ',1, WHITE)
            telaJogo.blit(text, (220, 7))

            font = pygame.font.Font(None, 40)
            text = font.render(str(contador), 1, WHITE)
            telaJogo.blit(text, (330, 7))

            #atualizacao
            font = pygame.font.Font(None, 40)
            text = font.render('Atualizacao:', 1, WHITE)
            telaJogo.blit(text, (380, 7))

            font = pygame.font.Font(None, 40)
            text = font.render(str(atualizacao), 1, WHITE)
            telaJogo.blit(text, (560, 7))

            #Todos os sprites
            all_sprites_list.draw(telaJogo)
            pygame.draw.line(telaJogo, WHITE, [0, 35], [800, 35], 2)

            pygame.display.flip()
            clock.tick(FPS)

        #Colisao com rebatedor___________________________________________________________________________________________________________________
        if rebatedor.rect.colliderect(bola.rect):
            pontos[0] += 1

            erro = 0                    #Zera e atualiza erro
            rede.atualizaPesos(erro)

            with open('dadosTreinamento.txt', 'a') as arquivo:
                arquivo.write('atualizacao: ' + str(atualizacao) +' '+ 'Erro: ' + str(erro) + "\n")

            if bola.movimento[1] < 0:
                bola.movimento[1] *= -1


        #Colisao com blocos_____________________________________________________________________________________________________________________
        blocos_collison_list = pygame.sprite.spritecollide(bola, todosBlocos, False)
        for blocos in blocos_collison_list:

            #Muda direção da bola
            if bola.rect.x + 5 < blocos.rect.x + Blocos_Dados.tamanhoX and bola.rect.x + 2*Bola_Dados.rad - 5 > blocos.rect.x:
                if bola.movimento[1] > 0:
                    bola.movimento[1] *= -1
            else:
                bola.movimento[0] *= -1

            #Conta pontos
                bola.velocidade += 0.1
                rebatedor.velocidade += 1.5
            blocos.kill()

            #Caso todos os blocos sejam destruidos eles são todos reconstruidos
            if len(todosBlocos) == 0:

                #Atualiza para exibir todas as alteracoes
                all_sprites_list.update()

                #Desenha
                telaJogo.fill(cor)

                #Pontuacao
                font = pygame.font.Font(None, 40)
                text = font.render('Pontos: ',1, WHITE)
                telaJogo.blit(text, (20, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(pontos[0]), 1, WHITE)
                telaJogo.blit(text, (130, 7))

                #vidas(contador)
                font = pygame.font.Font(None, 40)
                text = font.render('Mortes: ',1, WHITE)
                telaJogo.blit(text, (220, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(contador), 1, WHITE)
                telaJogo.blit(text, (330, 7))

                #atualizacao
                font = pygame.font.Font(None, 40)
                text = font.render('Atualizacao: ',1, WHITE)
                telaJogo.blit(text, (380, 7))

                font = pygame.font.Font(None, 40)
                text = font.render(str(atualizacao), 1, WHITE)
                telaJogo.blit(text, (560, 7))

                #Todos os sprites
                all_sprites_list.draw(telaJogo)
                pygame.draw.line(telaJogo, WHITE, [0, 35], [800, 35], 2)

                game(live)

        #Atualiza para exibir todas as alteracoes
        all_sprites_list.update()

        #Desenha
        telaJogo.fill(cor)

        #Pontuacao
        font = pygame.font.Font(None, 40)
        text = font.render('Pontos: ', 1, WHITE)
        telaJogo.blit(text, (20, 7))

        font = pygame.font.Font(None, 40)
        text = font.render(str(pontos[0]), 1, WHITE)
        telaJogo.blit(text, (130, 7))

        #vidas(contador)
        font = pygame.font.Font(None, 40)
        text = font.render('Mortes: ',1, WHITE)
        telaJogo.blit(text, (220, 7))

        font = pygame.font.Font(None, 40)
        text = font.render(str(contador), 1, WHITE)
        telaJogo.blit(text, (330, 7))

        #atualizacao
        font = pygame.font.Font(None, 40)
        text = font.render('Atualizacao: ',1 , WHITE)
        telaJogo.blit(text, (380, 7))

        font = pygame.font.Font(None, 40)
        text = font.render(str(atualizacao), 1, WHITE)
        telaJogo.blit(text, (560, 7))

        #Todos os sprites
        all_sprites_list.draw(telaJogo)
        pygame.draw.line(telaJogo, WHITE, [0, 35], [800, 35], 2)

        pygame.display.flip()
        clock.tick(FPS)

    else:
        pygame.quit() #Sai pygame
        sys.exit() #Deixa programa

if __name__ == '__main__':
    game(start)