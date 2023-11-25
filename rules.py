
from common import Point, Debugger, repr_direction
debug = Debugger(enable_log=False)

# 8방향에 대한 함수들
DIRECTIONS = [ 
    lambda x, y: (x+1, y), # dọc dưới #
    lambda x, y: (x+1, y+1), # chéo phải dưới #
    lambda x, y: (x+1, y-1), # chéo trái dưới
    lambda x, y: (x-1, y), # dọc trên
    lambda x, y: (x-1, y+1), # chéo phải trên
    lambda x, y: (x-1, y-1), # chéo trái trên
    lambda x, y: (x, y-1), # ngang trái
    lambda x, y: (x, y+1), # ngang phải #
]


def reverse_of(dir_func):
    """ 방향함수에 대한 역방향 함수를 리턴한다. """
    dx, dy = dir_func(0, 0)  # differentiate
    return lambda x, y: (x-dx, y-dy)


def is_outta_range(x, y):
    return x < 0 or x >= 19 or y < 0 or y >= 19


class Referee:
    """ 그 자리에 돌을 놓을 수 있는지, 누가 이겼는지를 판단하는 심판 클래스이다. """

    def __init__(self, initial_board, sizeBoard):
        self.board = initial_board
        self.last_move = (0, 0)
        self.sizeBoard = sizeBoard

    def update(self, x, y, player):
        self.board[y][x] = player
        self.last_move = (x, y)
        # print("Rule", self.board)


    # def determine(self):
    #     """ Determine who won.
    #     :return: player number who won. None if there's no winner (game isn't finished).
    #     """
    #     board = self.board
    #     x, y = self.last_move

    #     # check 8 directions and start backtracking.
    #     for dir_func in DIRECTIONS:
    #         nx, ny = dir_func(x, y) # xác định nó có thuộc điểm góc hay không
    #         if is_outta_range(nx, ny): continue # bỏ qua điểm góc

    #         if board[ny][nx] == board[y][x]: # cùng một người đánh
    #             # debug.log('Direction : ' + repr_direction(dir_func))
    #             # debug.log('Start at {}'.format(Point(x, y)))

    #             # to check properly, go to the end of direction
    #             while board[ny][nx] == board[y][x]:
    #                 nx, ny = dir_func(nx, ny)
    #                 if is_outta_range(nx, ny): break

    #             reverse_dir_func = reverse_of(dir_func)
    #             nx, ny = reverse_dir_func(nx, ny)  # one step back.

    #             # debug.log('End of direction : {}'.format(Point(nx, ny)))

    #             is_end = self._track(nx, ny, reverse_dir_func)
    #             if is_end:
    #                 # returns player who won.
    #                 return board[ny][nx]

    #             # debug.stop()

    # def _track(self, start_x, start_y, dir_func):
    #     x, y = start_x, start_y
    #     original_player = self.board[y][x]
    #     # debug.log('Track started at {}'.format(Point(x, y)))

    #     step = 1 # điểm cuối cùng luôn được tính
    #     while True:
    #         x, y = dir_func(x, y)
    #         if is_outta_range(x, y) or self.board[y][x] != original_player: # đụng góc hoặc khác người chơi
    #             if step == 6: return True
    #             # debug.log('Track finished at step {}'.format(step))
    #             return False
    #         step += 1

    #     # if step > 6:
    #     #     debug.log('Track success, but too many steps (step={})'.format(step))
    #     #     return False

    #     # return True

    def winner(self, turn):
        ##################################
        # vertical sequence detection
        ##################################
        
        # loop over board columns
        for col in range(self.sizeBoard):
            # define winning sequence list
            winning_sequence = []
            
            # loop over board rows
            for row in range(self.sizeBoard):
                # if found same next element in the row
                if self.board[row, col] == turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == 6:
                    # return the game is won state
                    return self.board[row, col]
        
        ##################################
        # horizontal sequence detection
        ##################################
        
        # loop over board columns
        for row in range(self.sizeBoard):
            # define winning sequence list
            winning_sequence = []
            
            # loop over board rows
            for col in range(self.sizeBoard):
                # if found same next element in the row
                if self.board[row, col] == turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == 6:
                    # return the game is won state
                    return self.board[row, col]
    
        ##################################
        # 1st diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(self.sizeBoard):
            # init column
            col = row
        
            # if found same next element in the row
            if self.board[row, col] == turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 6:
                # return the game is won state
                return self.board[row, col]
        
        ##################################
        # 2nd diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(self.sizeBoard):
            # init column
            col = self.sizeBoard - row - 1
        
            # if found same next element in the row
            if self.board[row, col] == turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 6:
                # return the game is won state
                return self.board[row, col]
        
        # by default return non winning state
        return None

    def can_place(self, row, column):
        if self.board[row][column] != 0:
            return False

        return True

    def undo(self, last_x, last_y, current_x, current_y, player):
        self.board[last_y][last_x] = player
        self.last_move = (current_x, current_y)
        print("Rule", self.board)

    def redo(self, current_x, current_y, player):
        self.board[current_y][current_x] = player
        self.last_move = (current_x, current_y)
        print("Rule", self.board)

