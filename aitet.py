from script.chl import ai as challenger
from script.chm import ai as champion
from tetris.game import game as referee
from tetris.defs import defs

from time import sleep

def main():
    newRef = referee()
    newChm = champion()
    newChl = challenger()
    
    while(True):
        chmMap, chlMap, curBlk, nexBlk = newRef.getData()
        chmPos, chmRot = newChm.compute(chmMap, chlMap, curBlk, nexBlk)
        chlPos, chlRot = newChl.compute(chlMap, chmMap, curBlk, nexBlk)
        if(newRef.compute(chmPos, chmRot, chlPos, chlRot)):
            newRef.printMap(newChm.CONST_NAME, newChl.CONST_NAME)
            break
        else:
            newRef.printMap(newChm.CONST_NAME, newChl.CONST_NAME)
            sleep(defs.GAME_SPEED)
            continue
    
    print("Game Over: "+newRef.reasonText)
    if newRef.isChmLost:
        print(newChm.CONST_NAME, "Lost!")
    if newRef.isChlLost:
        print(newChl.CONST_NAME, "Lost!")

if __name__ == "__main__":
    main()
