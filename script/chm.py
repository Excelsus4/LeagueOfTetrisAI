from time import sleep

class AI:
    # give your AI a name for display
    CONST_NAME = "ExcelsusE ver 1.1"

    def __init__(self):
        pass

    def shape_contour(self, degB):
        temporary = [-1]*4
        for idx in range(0, 4):
            for idy in range(0, 4):
                if degB[idx][idy]:
                    temporary[idx] = idy
        return temporary

    def calculate_match_score(self, conB, conM, position):
        ## Base Score
        matchScore = 44000
        lowestPoint = -1

        ## Best match 44000, minus 11000 for each hole
        listSum = []
        for idx in range(0, 4):
            if conB[idx] == -1:
                ## no need to consider blank line
                continue
            elif (position+idx < 0) or (position+idx > 9):
                ## this is part is out of limit while not a blank line
                return -400000
            else:
                # Finding the match sum Algorithm
                listSum.append(conB[idx] + conM[position+idx])
                # Finding the Lowest Point Algorithm
                if lowestPoint == -1:
                    lowestPoint = idx
                elif conB[idx] > conB[lowestPoint]:
                    lowestPoint = idx

        attatchSum = max(listSum)
        # if all printed value is equal, its a match
        for element in listSum:
            if element != attatchSum:
                # TODO: get the difference and calculate hole height
                matchScore -= 11000 * (attatchSum - element)

        # get the height of LOWEST POINT and give it multiple of 200
        # Lowest point is the one with highest Block Contour
        matchScore -= conM[position+lowestPoint] * 200

        # maybe highest point should be calculated from outside the function?
        
        return matchScore

    # method compute is mandatory for playing tetris
    def compute(self, myMap, opMap, current, next):
        # myMap is a 10 x 20 2D integer list representing the map for the player
        # opMap is the 10 x 20 2D integer list representing the map for the opponent player
        # map's origin is located on UPPERLEFT corner
        # list can be used like myMap[X][Y]
        
        # current is a 4 x 4 2D integer list representing current block's shape
        # next is the 4 x 4 2D integer list representing next block's shape
        # blocks rotate CLOCKWISE

        # Calculate block contour for all rotations
        degZ = current
        degO = list(zip(*degZ[::-1]))
        degD = list(zip(*degO[::-1]))
        degT = list(zip(*degD[::-1]))

        blockContour = self.shape_contour(degZ), self.shape_contour(degO), self.shape_contour(degD), self.shape_contour(degT)

        # Calculate map contour
        mapContour = [0]*10
        for idx in range(0, 10):
            for idy in range(0, 20):
                if myMap[idx][idy]:
                    mapContour[idx] = 20-idy
                    break

        #### Score Table: 
        ## -400000 for Suicide
        ## Best match 44000, minus 11000 for each hole
        ## 200 points for each y level
        ## 60 points for each top y level
        ## 1 points for each x level (it will start from right)

        ## Maybe reduce preferablity if there is hole underneath the point? like half the height score

        # Calculate score for each selections
        scoreSheet = [0] * 13 * 4

        for ids in range(0, 13*4):
                scoreSheet[ids] += 13 * 4 - ids
                #scoreSheet[ids] += ids

        # Match Check
        for idr in range(0,4):
            for idx in range(0, 13):
                scoreSheet[idr*13+idx] += self.calculate_match_score(blockContour[idr], mapContour, idx-3)

        # Fetch the max score position and rotation
        choosen = scoreSheet.index(max(scoreSheet))
        position = choosen%13
        rotation = int((choosen - position)/13)

        # return two signed integer values 
        # first integer is the position value which should range in -3 ~ 9 
        # and second integer is the rotation value range in 0 ~ 3
        # be careful that if block is out of index, your AI will lose immediately

        return position-3, rotation