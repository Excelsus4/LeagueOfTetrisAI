#!/usr/bin/env python3

from script.chl import AI as challenger
from script.chm import AI as champion
from tetris.game import Game as referee
from tetris import defs

from time import sleep

def main():
    newRef = referee()
    newChm = champion()
    newChl = challenger()
    
    while(True):
        chmMap, chlMap, curBlk, nexBlk = newRef.get_data()
        chmPos, chmRot = newChm.compute(chmMap, chlMap, curBlk, nexBlk)
        chlPos, chlRot = newChl.compute(chlMap, chmMap, curBlk, nexBlk)
        if(newRef.compute(chmPos, chmRot, chlPos, chlRot)):
            newRef.print_map(newChm.CONST_NAME, newChl.CONST_NAME)
            break
        else:
            newRef.print_map(newChm.CONST_NAME, newChl.CONST_NAME)
            sleep(defs.GAME_SPEED)
            continue
    
    print("Game Over: "+newRef.reasonText)
    if newRef.isChmLost:
        print(newChm.CONST_NAME, "Lost!")
    if newRef.isChlLost:
        print(newChl.CONST_NAME, "Lost!")

if __name__ == "__main__":
    main()
