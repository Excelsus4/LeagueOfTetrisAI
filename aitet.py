#!/usr/bin/env python3

from script.chl import AI as challenger
from script.chm import AI as champion
from tetris.game import Game as referee
from tetris import defs

from time import sleep


def main():
    new_ref = referee()
    new_chm = champion()
    new_chl = challenger()
    
    while True:
        chm_map, chl_map, cur_blk, nex_blk = new_ref.get_data()
        chm_pos, chm_rot = new_chm.compute(chm_map, chl_map, cur_blk, nex_blk)
        chl_pos, chl_rot = new_chl.compute(chl_map, chm_map, cur_blk, nex_blk)
        if new_ref.compute(chm_pos, chm_rot, chl_pos, chl_rot):
            new_ref.print_map(new_chm.CONST_NAME, new_chl.CONST_NAME)
            break
        else:
            new_ref.print_map(new_chm.CONST_NAME, new_chl.CONST_NAME)
            sleep(defs.GAME_SPEED)
            continue
    
    print("Game Over: "+new_ref.reason_text)
    if new_ref.is_chm_lost:
        print(new_chm.CONST_NAME, "Lost!")
    if new_ref.is_chl_lost:
        print(new_chl.CONST_NAME, "Lost!")


if __name__ == "__main__":
    main()
