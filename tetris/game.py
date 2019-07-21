from __future__ import print_function
import random

from . import defs
from . import term


class Game:
    def __init__(self):
        # Initialize clean new Game
        term.enable_color()
        self.chm_map = [[0] * (defs.Y_MAP_MAX+6) for _ in range(defs.X_MAP_MAX+6)]
        self.chl_map = [[0] * (defs.Y_MAP_MAX+6) for _ in range(defs.X_MAP_MAX+6)]
        self.cur_blk = random.sample(defs.BLK_LIB, 1)[0]
        self.cur_blk = self.rotate_block(self.nex_blk, random.randint(0,3))
        self.nex_blk = random.sample(defs.BLK_LIB, 1)[0]
        self.nex_blk = self.rotate_block(self.nex_blk, random.randint(0,3))
        self.push_blk()
        self.is_chm_lost = False
        self.is_chl_lost = False
        self.reason_text = ""
        for idy in range(3 + defs.Y_MAP_MAX, 6 + defs.Y_MAP_MAX):
            for idx in range(3, 3 + defs.X_MAP_MAX):
                self.chm_map[idx][idy] = -1
                self.chl_map[idx][idy] = -1

    def push_blk(self):
        self.cur_blk = self.nex_blk
        self.nex_blk = random.sample(defs.BLK_LIB, 1)[0]
        self.nex_blk = self.rotate_block(self.nex_blk, random.randint(0,3))

    def get_data(self):
        # print(self.chm_map)
        # print()
        # TODO: fix the problem of crop
        sub_chm = [seq[3:defs.Y_MAP_MAX+3] for seq in self.chm_map[3:defs.X_MAP_MAX+3]]
        sub_chl = [seq[3:defs.Y_MAP_MAX+3] for seq in self.chl_map[3:defs.X_MAP_MAX+3]]

        return sub_chm, sub_chl, self.cur_blk, self.nex_blk

    def compute(self, chm_pos, chm_rot, chl_pos, chl_rot):
        # compute new map using information returned by each AI
        self.is_chm_lost, self.chm_map = self.compute_map(self.chm_map, chm_pos + 3, self.rotate_block(self.cur_blk, chm_rot))
        self.is_chl_lost, self.chl_map = self.compute_map(self.chl_map, chl_pos + 3, self.rotate_block(self.cur_blk, chl_rot))
        return self.is_chm_lost or self.is_chl_lost
    
    def compute_map(self, b_map, pos, block):
        clr = True
        y_pos = 0

        # Block Drop
        while True:
            for idy in range(0, 4):
                for idx in range(0, 4):
                    if block[idx][idy] and b_map[idx+pos][idy+y_pos]:
                        clr = False
            
            if clr:
                y_pos += 1
                continue
            else:
                y_pos -= 1
                break

        for idy in range(0, 4):
            for idx in range(0, 4):
                if block[idx][idy]:
                    b_map[idx+pos][idy+y_pos] = block[idx][idy]

        # Full Line Check
        line_flag = True

        while line_flag:
            line_flag = False
            for idy in range(3, defs.Y_MAP_MAX+3):
                hole_flag = False
                for idx in range(3, defs.X_MAP_MAX+3):
                    if not b_map[idx][idy]:
                        hole_flag = True
                        break
                if not hole_flag:
                    for ldy in range(idy, 0, -1):
                        for idx in range(3, defs.X_MAP_MAX+3):
                            b_map[idx][ldy] = b_map[idx][ldy-1]
                    line_flag = True
                    break

        clr = False

        # Top Check
        for idy in range(0, 3):
            for idx in range(3, defs.X_MAP_MAX+3):
                if b_map[idx][idy]:
                    clr = True
                    self.reason_text = "Tower is too high!"

        # Bound Check
        for idy in range(0, defs.Y_MAP_MAX+6):
            for idx in range(0, 3):
                if b_map[idx][idy] or b_map[idx+defs.X_MAP_MAX+3][idy]:
                    clr = True
                    self.reason_text = "Block Out of Bound!"

        return clr, b_map

    def rotate_block(self, target_block, times):
        # Clockwise 90deg Rotate
        if times == 0:
            return target_block
        else:
            return self.rotate_block(list(zip(*target_block[::-1])), times-1)

    @staticmethod
    def print_brick(brick_code):
        if brick_code == -1:
            print('\33[37m'+'\33[40m' + "▩", end="")
        elif brick_code == -2:
            print('\33[37m'+'\33[40m' + "　", end="")
        elif brick_code:
            if brick_code == 1:
                print('\33[41m'," ", end="")
            elif brick_code == 2:
                print('\33[42m'," ", end="")
            elif brick_code == 3:
                print('\33[105m'," ", end="")
            elif brick_code == 4:
                print('\33[104m'," ", end="")
            elif brick_code == 5:
                print('\33[45m'," ", end="")
            elif brick_code == 6:
                print('\33[46m'," ", end="")
            elif brick_code == 7:
                print('\33[101m'," ", end="")
        else:
            print('\33[37m'+'\33[40m',".", end="")

    def print_map(self, chm_name, chl_name):
        self.push_blk()
        term.clear_screen()
        print(chm_name + " vs " + chl_name)
        # Top
        for _ in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        for _ in range(0, defs.X_BLK_MAX):
            self.print_brick(-2)
        for _ in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)

        # In between
        for idy in range(0, defs.Y_MAP_MAX):
            print("")
            # Champion Map
            self.print_brick(-1)
            for idx in range(0, defs.X_MAP_MAX):
                self.print_brick(self.chm_map[idx+3][idy+3])
            self.print_brick(-1)
            # Block Indicator
            if idy < 1:
                for _ in range(0, 4):
                    self.print_brick(-1)
            elif idy < 1 + defs.Y_BLK_MAX:
                for idx in range(0, 4):
                    # Current Block
                    self.print_brick(self.cur_blk[idx][idy-1])
            elif idy < 2 + defs.Y_BLK_MAX:     
                for _ in range(0, 4):
                    self.print_brick(-1)
            elif idy < 2 + defs.Y_BLK_MAX * 2:
                for idx in range(0, 4):
                    # Next Block
                    self.print_brick(self.nex_blk[idx][idy-10])
            elif idy < 3 + defs.Y_BLK_MAX * 2:
                for _ in range(0, 4):
                    self.print_brick(-1)
            else:
                for _ in range(0, 4):
                    self.print_brick(-2)
            self.print_brick(-1)
            # Challenger Map
            for idx in range(0, defs.X_MAP_MAX):
                self.print_brick(self.chl_map[idx+3][idy+3])
            self.print_brick(-1)
        print("")
        # Bottom
        for _ in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        for _ in range(0, defs.X_BLK_MAX):
            self.print_brick(-2)
        for _ in range(0, defs.X_MAP_MAX+2):
            self.print_brick(-1)
        print("")
