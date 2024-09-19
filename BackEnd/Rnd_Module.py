import hashlib

def make_hash(di):
    return hashlib.sha256(di.encode()).hexdigest()

class Random_Module:

    def __init__(self,seed):
        self.seed = seed

    def rnd(self,max):
        output = int(make_hash(self.seed)[:8], 16) % max
        self.seed = make_hash(self.seed + str(output))
        return output