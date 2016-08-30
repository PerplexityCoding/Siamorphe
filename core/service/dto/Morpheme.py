# -*- coding: utf-8 -*-

import json

class Morpheme:
    def __init__(self, base, inflected, pos, subPos, read, rank = 0, score = 0, id = -1):
        if id == -1:
            id = hash((pos, subPos, read, base))
        self.id = id
        self.pos = pos
        self.subPos = subPos
        self.read = read
        self.base = base
        self.rank = rank
        self.score = score

    def __ne__(self, o):
        return not self.__eq__(o)
        
    def __eq__(self, o):
        if not isinstance(o, Morpheme): return False
        if self.id != o.id: return False
        return True

    def __hash__(self):
        return self.id
        
    def __repr__(self):
        u = unicode(self.base)
        return "base:" + u.encode('utf-8') + " - rank: " + str(self.rank) + " - score " + str(self.score)
