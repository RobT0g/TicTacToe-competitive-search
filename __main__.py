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
        freespaces = [[], [], [], []]
        scores = []
        gridcpy = [[j.copy() for j in self.grid] for i in range(5)]
        for k1, v1 in enumerate(self.grid):
            for k2, v2 in enumerate(v1):
                if v2 == 0:
                    for i in freespaces:
                        i.append((k1, k2))
                    scores.append(0)
        # Lógica
        for k, v in enumerate(freespaces[0]):
            gridcpy[1][v[0]][v[1]] = 1
            res = self.checkFinished(gridcpy[1])
            if res[0]:
                scores[k] = 1
                continue
            gridcpy[2][v[0]][v[1]] = 1
            freespaces[1].pop(k)
            for k1, v1 in enumerate(freespaces[1]):
                gridcpy[2] = self.genGridCopy(gridcpy[1])
                gridcpy[3] = self.genGridCopy(gridcpy[1])
                freespaces[2] = freespaces[1].copy()
                gridcpy[2][v1[0]][v1[1]] = -1
                res = self.checkFinished(gridcpy[2])
                if res[0]:
                    scores[k] = -1
                    break
                elif scores[k] == 1:
                    continue
                gridcpy[3][v1[0]][v1[1]] = 1
                freespaces[2].pop(k1)
                for k2, v2 in enumerate(freespaces[2]):
                    gridcpy[3] = self.genGridCopy(gridcpy[2])
                    gridcpy[3][v2[0]][v2[1]] = 1
                    res = self.checkFinished(gridcpy[3])
                    if res[0]:
                        scores[k] = 1
                        break
            gridcpy[1] = self.genGridCopy(gridcpy[0])
            gridcpy[2] = self.genGridCopy(gridcpy[0])
            gridcpy[3] = self.genGridCopy(gridcpy[0])
            freespaces[1] = freespaces[0].copy()
            freespaces[2] = freespaces[0].copy()
        try:
            return freespaces[0][scores.index(1)]
        except: pass
        try:
            return freespaces[0][scores.index(0)]
        except: pass
        return freespaces[0][0]    

    def play(self):
        pos = self.recoursiveTest(self.grid)
        moves = [i[0] if i[2] == -1 else 0 for i in pos]
        for i in range(3):
            for k, v in enumerate(mov):
                pass

    def recoursiveTest(self, modgrid, comturn = True):
        results = []
        for k1, v1 in modgrid:
            for k2, v2 in v1:
                if v2 == 0:
                    results.append([(k1, k2), self.genGridCopy(modgrid), 0])
                    results[-1][1][k1][k2] = 1 if comturn else -1
                    results[-1][2] = self.checkFinished(results[-1][1])[1]
        return results
        
        

    def genGridCopy(self, grid):
        return [i.copy() for i in grid]

    def checkFinished(self, totest=False):
        grid = totest if totest else self.grid

        for i in range(3):
            x = [grid[i][i] != 0, grid[i][i]]
            y = [grid[i][i] != 0, grid[i][i]]
            if not (x[0] or y[0]):
                continue
            for j in range(3):
                if x[0]:
                    x[0] = x[0] and grid[i][j] == x[1]
                if y[0]:
                    y[0] = y[0] and grid[j][i] == x[1]
            if x[0] or y[0]:
                return [True, x[1] if x[1] else y[1]]
        x = [grid[0][0] != 0, grid[0][0]]
        y = [grid[0][2] != 0, grid[0][2]]
        for i in range(1, 3):
            x[0] = x[0] and grid[i][i] == x[1]
            y[0] = y[0] and grid[i][2-i] == y[1]
        if x[0] or y[0]:
            return [True, x[1] if x[1] else y[1]]
        return [False, 0]

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        for k1, v1 in enumerate(self.grid):
            for k2, v2 in enumerate(v1):
                if v2 == 0:
                    continue
                self.display.blit(self.marks[0 if v2 == -1 else 1], (16+k1*64, 16+k2*64))
        if self.won != 0:
            self.display.blit(self.finishedMsg, (16, 16+64))
        pygame.display.flip()
    
    def update(self):
        if self.won != 0 or (not self.playerTurn):
            return
        pressed = list(map(lambda x: (x-16)//64, pygame.mouse.get_pos()))
        if not self.grid[pressed[0]][pressed[1]]:
            self.grid[pressed[0]][pressed[1]] = -1 if self.playerTurn else 1
            self.playerTurn = False
        self.putOnScreen()
        if (r:=self.checkFinished())[0]:
            self.won = r[1]
            self.putOnScreen()
        else:
            m = self.comPlay()
            self.grid[m[0]][m[1]] = 1
            if (r:=self.checkFinished())[0]:
                self.won = r[1]
            else:
                self.playerTurn = True
            self.putOnScreen()

def main():
    pygame.init()  
    el = TicTac()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                el.update()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False 
            if pygame.key.get_pressed()[pygame.K_SPACE] and el.won != 0:
                el = TicTac()

if __name__ == '__main__':
    main()
