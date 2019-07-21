class AI:
    # give your AI a name for display
    CONST_NAME = "plusTwoModEightBot"

    def __init__(self):
        self.temp = 6

    # method compute is mandatory for playing tetris
    def compute(self, myMap, opMap, current, next):
        # myMap is a 10 x 20 2D integer list representing the map for the player
        # opMap is the 10 x 20 2D integer list representing the map for the opponent player
        # map's origin is located on UPPERLEFT corner
        
        # current is a 4 x 4 2D integer list representing current block's shape
        # next is the 4 x 4 2D integer list representing next block's shape
        # blocks rotate CLOCKWISE

        # TODO: implement your algorithm here
        self.temp = (self.temp + 2) % 8

        # return two signed integer values 
        # first integer is the position value which should range in -3 ~ 19 
        # and second integer is the rotation value range in 0 ~ 3
        # be careful that if block is out of index, your AI will lose immediately
        return self.temp, 0