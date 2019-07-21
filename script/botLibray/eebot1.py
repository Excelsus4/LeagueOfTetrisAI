class AI:
    # give your AI a name for display
    CONST_NAME = "ExcelsusE ver 1.1"

    def __init__(self):
        pass

    @staticmethod
    def shape_contour(deg_b):
        temporary = [-1]*4
        for idx in range(0, 4):
            for idy in range(0, 4):
                if deg_b[idx][idy]:
                    temporary[idx] = idy
        return temporary

    @staticmethod
    def calculate_match_score(con_block, con_map, position):
        # Base Score
        match_score = 44000
        lowest_point = -1

        # Best match 44000, minus 11000 for each hole
        list_sum = []
        for idx in range(0, 4):
            if con_block[idx] == -1:
                # no need to consider blank line
                continue
            elif (position+idx < 0) or (position+idx > 9):
                # this is part is out of limit while not a blank line
                return -400000
            else:
                # Finding the match sum Algorithm
                list_sum.append(con_block[idx] + con_map[position+idx])
                # Finding the Lowest Point Algorithm
                if lowest_point == -1:
                    lowest_point = idx
                elif con_block[idx] > con_block[lowest_point]:
                    lowest_point = idx

        attach_sum = max(list_sum)
        # if all printed value is equal, its a match
        for element in list_sum:
            if element != attach_sum:
                match_score -= 11000 * (attach_sum - element)

        # get the height of LOWEST POINT and give it multiple of 200
        # Lowest point is the one with highest Block Contour
        match_score -= con_map[position+lowest_point] * 200

        # maybe highest point should be calculated from outside the function?
        
        return match_score

    # method compute is mandatory for playing tetris
    def compute(self, my_map, op_map, current, next):
        # my_map is a 10 x 20 2D integer list representing the map for the player
        # op_map is the 10 x 20 2D integer list representing the map for the opponent player
        # map's origin is located on UPPERLEFT corner
        # list can be used like my_map[X][Y]
        
        # current is a 4 x 4 2D integer list representing current block's shape
        # next is the 4 x 4 2D integer list representing next block's shape
        # blocks rotate CLOCKWISE

        # Calculate block contour for all rotations
        deg_z = current
        deg_o = list(zip(*deg_z[::-1]))
        deg_d = list(zip(*deg_o[::-1]))
        deg_t = list(zip(*deg_d[::-1]))

        block_contour = \
            self.shape_contour(deg_z), self.shape_contour(deg_o), self.shape_contour(deg_d), self.shape_contour(deg_t)

        # Calculate map contour
        map_contour = [0]*10
        for idx in range(0, 10):
            for idy in range(0, 20):
                if my_map[idx][idy]:
                    map_contour[idx] = 20-idy
                    break

        # Score Table:
        # -400000 for Suicide
        # Best match 44000, minus 11000 for each hole
        # 200 points for each y level
        # 60 points for each top y level
        # 1 points for each x level (it will start from right)

        # Maybe reduce preferably if there is hole underneath the point? like half the height score

        # Calculate score for each selections
        score_sheet = [0] * 13 * 4

        for ids in range(0, 13*4):
            score_sheet[ids] += 13 * 4 - ids
            # score_sheet[ids] += ids

        # Match Check
        for idr in range(0,4):
            for idx in range(0, 13):
                score_sheet[idr*13+idx] += self.calculate_match_score(block_contour[idr], map_contour, idx-3)

        # Fetch the max score position and rotation
        chosen = score_sheet.index(max(score_sheet))
        position = chosen % 13
        rotation = int((chosen - position)/13)

        # return two signed integer values 
        # first integer is the position value which should range in -3 ~ 9 
        # and second integer is the rotation value range in 0 ~ 3
        # be careful that if block is out of index, your AI will lose immediately

        return position-3, rotation
