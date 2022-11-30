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
    
    def genEndGameMsg(self):
        self.finishedMsg = pygame.Surface((64*3, 64), pygame.SRCALPHA, 32)
        msg = 'You '
        if self.won == 1:
            msg += 'lose.'
        elif self.won == -1:
            msg += 'win.'
        else:
            msg += 'draw.'
        txt = self.font.render(msg, False, (255, 255, 255))
        s = txt.get_size()
        pygame.draw.rect(self.finishedMsg, (50, 50, 50), pygame.Rect((32*3)-((s[0]+20)/2), 32-((s[1]+10)/2), s[0]+20, s[1]+10))
        self.finishedMsg.blit(txt, ((32*3)-(s[0]/2), 32-(s[1]/2)))

    def play(self):
        [moves, grid, scores] = self.recoursiveTest(self.grid)
        for k, v in enumerate(scores):
            if v != 0:
                if v == 1:
                    return moves[k]
                continue
            grids = [grid[k]]
            for i in range(2):
                [res, grids] = self.testGrids(grids, i%2 == 1)
                if res:
                    scores[k] = grids
                    break
        try:
            return moves[scores.index(1)]
        except: pass
        try:
            if scores[moves.index((1, 1))] == 0:
                return (1, 1)
        except: pass
        try:
            for k, i in enumerate(moves):
                if ((i[0]+i[1])%2 == 0) and scores[k] == 0:
                    return i
        except: pass
        try:
            return moves[scores.index(0)]
        except: pass
        return moves[0]

    def testGrids(self, gridlist, comturn):
        #print('-------- TESTING ---------')
        #print(f'amnt: {len(gridlist)}, turn: {comturn}')
        nextGrids = []
        for i in gridlist:
            [nmv, ngrid, nscore] = self.recoursiveTest(i, comturn)
            #print(i)
            #print(f'> {nscore}')
            for k, v in enumerate(nscore):
                if v == 0:
                    nextGrids.append(ngrid[k])
                    continue
                #print(nmv[k], ngrid[k], v)
                return [True, v]
        return [False, nextGrids]

    def recoursiveTest(self, modgrid, comturn = True):
        data = [[], [], []]
        for k1, v1 in enumerate(modgrid):
            for k2, v2 in enumerate(v1):
                if v2 == 0:
                    data[0].append((k1, k2))
                    data[1].append(self.genGridCopy(modgrid))
                    data[1][-1][k1][k2] = 1 if comturn else -1
                    data[2].append((x:=self.checkFinished(data[1][-1])[1]))
        return data
    
    def genGridCopy(self, grid):
        return [i.copy() for i in grid]

    def checkFinished(self, totest=False):
        grid = totest if totest else self.grid
        nozero = True
        for i in grid:
            if 0 in i:
                nozero = False
                break
        if nozero:
            return [True, 2]
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
            return [True, x[1] if x[0] else y[1]]
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
            self.grid[pressed[0]][pressed[1]] = -1
            self.playerTurn = False
        self.putOnScreen()
        if (r:=self.checkFinished())[0]:
            self.won = r[1]
            self.genEndGameMsg()
            self.putOnScreen()
        else:
            m = self.play()
            self.grid[m[0]][m[1]] = 1
            if (r:=self.checkFinished())[0]:
                self.won = r[1]
                self.genEndGameMsg()
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
