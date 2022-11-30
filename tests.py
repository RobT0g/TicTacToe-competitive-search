from main import TicTac
import pygame
import random

pygame.init()

x = TicTac()
print(x.checkFinished([[1, 1, -1], [0, -1, 0], [-1, 0, 0]]))
'''examples = [[[random.randint(-1, 1) for i in range(3)] for j in range(3)] for k in range(20)]
for i in examples:
    print(f'{i} - {x.checkFinished(i)}')'''