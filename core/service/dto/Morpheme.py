# -*- coding: utf-8 -*-

import json

class Morpheme:
    def __init__(self, base, inflected, pos, subPos, read, score = 0, baseScore = 0, id = -1):
        if id == -1:
            id = hash((pos, subPos, read, base))
        self.id = id
        self.pos = pos
        self.subPos = subPos
        self.read = read
        self.base = base
        self.baseScore = baseScore
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
        return "#Morpheme# base:" + u.encode('utf-8') + " - baseScore: " + str(self.baseScore) + " - score " + str(self.score)
