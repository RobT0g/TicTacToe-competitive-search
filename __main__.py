import pygame

class TicTac:
    def __init__(self) -> None:
        self.size = (64*3+32, 64*3+32)
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Tic Tac Toe')
        self.playerTurn = True
        self.won = 0
        self.font = pygame.font.SysFont('Times New Roman', 20)
        self.grid = [[0 for i in range(3)] for j in range(3)]
        self.genFrame()
        self.putOnScreen()
    
    def genFrame(self):
        self.frame = pygame.Surface(self.size)
        pygame.draw.rect(self.frame, (55, 71, 79), pygame.Rect(0, 0, *self.size))
        pygame.draw.rect(self.frame, (20, 20, 20), pygame.Rect(0, 0, *self.size), 16)
        pygame.draw.rect(self.frame, (50, 50, 50), pygame.Rect(0, 0, *self.size), 1)
        pygame.draw.line(self.frame, (0, 0, 0), (17, 16+64), (13+64*3, 16+64), 2)
        pygame.draw.line(self.frame, (0, 0, 0), (17, 16+64*2), (13+64*3, 16+64*2), 2)
        pygame.draw.line(self.frame, (0, 0, 0), (16+64, 17), (16+64, 13+64*3), 2)
        pygame.draw.line(self.frame, (0, 0, 0), (16+64*2, 17), (16+64*2, 13+64*3), 2)
        self.marks = [pygame.Surface((64, 64), pygame.SRCALPHA, 32) for i in range(2)]
        pygame.draw.line(self.marks[0], (255, 255, 255), (4, 4), (60, 60), 3)
        pygame.draw.line(self.marks[0], (255, 255, 255), (4, 60), (60, 4), 3)
        pygame.draw.circle(self.marks[1], (255, 255, 255), (31, 31), 28, 3)
        self.finishedMsg = pygame.Surface((64*3, 64), pygame.SRCALPHA, 32)
        txt = self.font.render(f'''You {'win' if self.won == 1 else 'lose'}.''', False, (255, 255, 255))
        s = txt.get_size()
        pygame.draw.rect(self.finishedMsg, (50, 50, 50), pygame.Rect((32*3)-((s[0]+20)/2), 32-((s[1]+10)/2), s[0]+20, s[1]+10))
        self.finishedMsg.blit(txt, ((32*3)-(s[0]/2), 32-(s[1]/2)))

    def comPlay(self):
        pass

    def checkFinished(self):
        for i in range(3):
            x = [self.grid[i][i] != 0, self.grid[i][i]]
            y = [self.grid[i][i] != 0, self.grid[i][i]]
            if not (x[0] or y[0]):
                continue
            for j in range(3):
                if x[0]:
                    x[0] = x[0] and self.grid[i][j] == x[1]
                if y[0]:
                    y[0] = y[0] and self.grid[j][i] == x[1]
            if x[0] or y[0]:
                self.won = x[1] if x[1] else y[1]
                print('Finished!')
        x = [self.grid[0][0] != 0, self.grid[0][0]]
        y = [self.grid[0][2] != 0, self.grid[0][2]]
        for i in range(1, 3):
            x[0] = x[0] and self.grid[i][i] == x[1]
            y[0] = y[0] and self.grid[i][2-i] == y[1]
        if x[0] or y[0]:
            self.won = x[1] if x[1] else y[1]
            print('Finished!')

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        for k1, v1 in enumerate(self.grid):
            for k2, v2 in enumerate(v1):
                if v2 == 0:
                    continue
                self.display.blit(self.marks[v2-1], (16+k1*64, 16+k2*64))
        if self.won != 0:
            self.display.blit(self.finishedMsg, (16, 16+64))
        pygame.display.flip()
    
    def update(self):
        if self.won != 0 or (not self.playerTurn):
            return
        pressed = list(map(lambda x: (x-16)//64, pygame.mouse.get_pos()))
        if not self.grid[pressed[0]][pressed[1]]:
            self.grid[pressed[0]][pressed[1]] = 1 if self.playerTurn else 2
            self.playerTurn = False
        self.putOnScreen()
        self.checkFinished()
        self.comPlay()

def main():
    pygame.init()  
    el = TicTac()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                el.update()
                el.putOnScreen()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False 
            if pygame.key.get_pressed()[pygame.K_SPACE] and el.won != 0:
                el = TicTac()

if __name__ == '__main__':
    main()
