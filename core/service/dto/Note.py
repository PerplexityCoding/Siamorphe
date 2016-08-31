from core.utils.utils import fieldChecksum

class Note:

    def __init__(self, id, expression, knowledgeLevel, lastUpdated = None, expressionCsum = None, score = 0, difficultyScore = 0):
        self.id = id
        self.expression = expression
        self.knowledgeLevel = knowledgeLevel
        self.lastUpdated = lastUpdated

        if expressionCsum == None:
            self.expressionCsum = fieldChecksum(expression)

        self.score = score
        self.difficultyScore = difficultyScore #between 0 and 100

    def __repr__(self):
        u = unicode(self.expression)
        return "#Note#" + str(self.id) + " " + u.encode('utf-8')  + " " + str(self.knowledgeLevel)  + " " + str(self.lastUpdated)  +\
               " " + str(self.expressionCsum)  + " " + str(self.score);
