import hashlib
import time

def make_hash(di):
    return hashlib.sha256(di.encode()).hexdigest()

class Random_Module:

    def __init__(self,seed):
        self.seed = seed

    def rnd(self,max):
        output = int(make_hash(self.seed)[:8], 16) % max
        self.seed = make_hash(self.seed + str(output) + str(time.time()))
        return output

RM = Random_Module('Seed_2525' + str(time.time()))



def shuffle_puzzle(w,h):
    board = [[[i,e] for e in range(h)] for i in range(w)]
    for i in range(100):
        x = RM.rnd(w)
        y = RM.rnd(h)
        
        mv_x =  1 - 1 * RM.rnd(2)
        mv_y =  1 - 1 * RM.rnd(2)

        if x + mv_x < 0 or x + mv_x >= w:
            mv_x = -mv_x
        if y + mv_y < 0 or y + mv_y >= h:
            mv_y = -mv_y
        
        status = board[x][y]
        board[x][y] = board[x + mv_x][y + mv_y]
        board[x + mv_x][y + mv_y] = status
    return board






