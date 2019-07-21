import random

from . import defs
from . import term

class Game:
    def __init__(self):
        # Initialize clean new Game
        term.enable_color()
        self.chmMap = [[0] * (defs.Y_MAP_MAX+6) for _ in range(defs.X_MAP_MAX+6)]
        self.chlMap = [[0] * (defs.Y_MAP_MAX+6) for _ in range(defs.X_MAP_MAX+6)]
        self.nexBlk = random.sample(defs.BLK_LIB, 1)[0]
        self.nexBlk = self.rotate_block(self.nexBlk, random.randint(0,3))
        self.push_blk()
        self.isChmLost = False
        self.isChlLost = False
        self.reasonText = ""
        for idy in range(3 + defs.Y_MAP_MAX, 6 + defs.Y_MAP_MAX):
            for idx in range(3, 3 + defs.X_MAP_MAX):
                self.chmMap[idx][idy] = -1
                self.chlMap[idx][idy] = -1

    def push_blk(self):
        self.curBlk = self.nexBlk
        self.nexBlk = random.sample(defs.BLK_LIB, 1)[0]
        self.nexBlk = self.rotate_block(self.nexBlk, random.randint(0,3))

    def get_data(self):
        # print(self.chmMap)
        # print()
        # TODO: fix the problem of crop
        subChm = [seq[3:defs.Y_MAP_MAX+3] for seq in self.chmMap[3:defs.X_MAP_MAX+3]]
        subChl = [seq[3:defs.Y_MAP_MAX+3] for seq in self.chlMap[3:defs.X_MAP_MAX+3]]

        return subChm, subChl, self.curBlk, self.nexBlk

    def compute(self, chmPos, chmRot, chlPos, chlRot):
        # compute new map using information returned by each AI
        self.isChmLost, self.chmMap = self.compute_map(self.chmMap, chmPos + 3, self.rotate_block(self.curBlk, chmRot))
        self.isChlLost, self.chlMap = self.compute_map(self.chlMap, chlPos + 3, self.rotate_block(self.curBlk, chlRot))
        return self.isChmLost or self.isChlLost
    
    def compute_map(self, bmap, pos, block):
        clr = True
        ypos = 0

        # Block Drop
        while True:
            for idy in range(0, 4):
                for idx in range(0, 4):
                    if(block[idx][idy] and bmap[idx+pos][idy+ypos]):
                        clr = False
            
            if clr:
                ypos += 1
                continue
            else:
                ypos -= 1
                break

        for idy in range(0, 4):
            for idx in range(0, 4):
                if(block[idx][idy]):
                    bmap[idx+pos][idy+ypos] = block[idx][idy]

        # Full Line Check
        holeFlag = False
        lineFlag = True

        while lineFlag:
            lineFlag = False
            for idy in range(3, defs.Y_MAP_MAX+3):
                holeFlag = False
                for idx in range(3, defs.X_MAP_MAX+3):
                    if not bmap[idx][idy]:
                        holeFlag = True
                        break
                if not holeFlag:
                    for ldy in range(idy, 0, -1):
                        for idx in range(3, defs.X_MAP_MAX+3):
                            bmap[idx][ldy] = bmap[idx][ldy-1]
                    lineFlag = True
                    break

        clr = False

        # Top Check
        for idy in range(0, 3):
            for idx in range(3, defs.X_MAP_MAX+3):
                if bmap[idx][idy]:
                    clr = True
                    self.reasonText = "Tower is too high!"

        # Bound Check
        for idy in range(0, defs.Y_MAP_MAX+6):
            for idx in range(0, 3):
                if bmap[idx][idy] or bmap[idx+defs.X_MAP_MAX+3][idy]:
                    clr = True
                    self.reasonText = "Block Out of Bound!"

        return clr, bmap

    def rotate_block(self, targetBlock, times):
        # Clockwise 90deg Rotate
        if times == 0:
            return targetBlock
        else:
            return self.rotate_block(list(zip(*targetBlock[::-1])), times-1)

    def print_brick(self, brickCode):
        if brickCode == -1:
            print('\33[37m'+'\33[40m' + "▩", end="")
        elif brickCode == -2:
            print('\33[37m'+'\33[40m' + "　", end="")
        elif brickCode:
            if brickCode == 1:
                print('\33[41m'," ", end="")
            elif brickCode == 2:
                print('\33[42m'," ", end="")
            elif brickCode == 3:
                print('\33[105m'," ", end="")
            elif brickCode == 4:
                print('\33[104m'," ", end="")
            elif brickCode == 5:
                print('\33[45m'," ", end="")
            elif brickCode == 6:
                print('\33[46m'," ", end="")
            elif brickCode == 7:
                print('\33[101m'," ", end="")
        else:
            print('\33[37m'+'\33[40m',".", end="")

    def print_map(self, chmName, chlName):
        self.push_blk()
        term.clear_screen()
        print(chmName + " vs " + chlName)
        # Top
        for idx in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        for idx in range(0, defs.X_BLK_MAX):
            self.print_brick(-2)
        for idx in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)

        # In between
        for idy in range(0, defs.Y_MAP_MAX):
            print("")
            # Champion Map
            self.print_brick(-1)
            for idx in range(0, defs.X_MAP_MAX):
                self.print_brick(self.chmMap[idx+3][idy+3])
            self.print_brick(-1)
            # Block Indicator
            if idy < 1:
                for idx in range(0, 4):
                    self.print_brick(-1)
            elif idy < 1 + defs.Y_BLK_MAX:
                for idx in range(0, 4):
                    # Current Block
                    self.print_brick(self.curBlk[idx][idy-1])
            elif idy < 2 + defs.Y_BLK_MAX:     
                for idx in range(0, 4):
                    self.print_brick(-1)
            elif idy < 2 + defs.Y_BLK_MAX * 2:
                for idx in range(0, 4):
                    # Next Block
                    self.print_brick(self.nexBlk[idx][idy-10])
            elif idy < 3 + defs.Y_BLK_MAX * 2:
                for idx in range(0, 4):
                    self.print_brick(-1)
            else:
                for idx in range(0, 4):
                    self.print_brick(-2)
            self.print_brick(-1)
            # Challenger Map
            for idx in range(0, defs.X_MAP_MAX):
                self.print_brick(self.chlMap[idx+3][idy+3])
            self.print_brick(-1)
        print("")
        # Bottom
        for idx in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        for idx in range(0, defs.X_BLK_MAX):
            self.print_brick(-2)
        for idx in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        print("")