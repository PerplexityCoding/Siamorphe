
import logging
from core.utils.utils import getList

class MorphemesService:
    def __init__(self):
        logging.debug("init morphemes base")

    def analyzeNotes(self, notes):

        morphemes = self.extactMorphemesFromNotes(notes)

        self.createKanjiDicts(notes)
        self.refreshMorphemesKnowledgeLevel(notes)
        self.computeMorphemesScore(morphemes)
        self.computeNotesScore(notes)

    def extactMorphemesFromNotes(self, notes):

        logging.debug("Extract Morphemes")
        morphemesById = dict()

        for note in notes:
            expression = note.expression
            #logging.debug(expression)

            morphemes = self.extractMorphemes(expression)
            noteMorphemes = set() # prevent duplicate morphemes in sentence
            for morpheme in morphemes:
                morphemeId = morpheme.id
                if morphemeId in morphemesById:
                    morpheme = morphemesById[morphemeId]
                else:
                    morphemesById[morphemeId] = morpheme
                noteMorphemes.add(morpheme)
            note.morphemes = noteMorphemes

        self.morphemesById = morphemesById

        allUniqueMorphemes = getList(morphemesById)
        allUniqueMorphemes = self.filterMorphemes(allUniqueMorphemes)

        logging.debug("Extract Morphemes: Done")

        return allUniqueMorphemes

    def refreshMorphemesKnowledgeLevel(self, notes):

        #logging.debug(notes)

        logging.debug("refreshMorphemesKnowledgeLevel")

        for note in notes:
            for morpheme in note.morphemes:
                morpheme.knowledgeLevel = max(morpheme.knowledgeLevel, note.knowledgeLevel)
                #logging.debug(morpheme)

        logging.debug("refreshMorphemesKnowledgeLevel: Done")

        #logging.debug(notes)

    def computeNotesScore(self, notes):

        if notes == None:
            return None

        logging.debug("Compute Notes " + str(len(notes)))

        modifiedNotes = list()
        for note in notes:
            morphemes = note.morphemes
            score = 0
            for morpheme in morphemes:
                score += (morpheme.score + morpheme.baseScore)

            if note.score == 0 or note.score == None or abs(int(note.score) - int(score)) >= 15: #see if changing it every time is slow now
                note.score = score
                if score >= 1000:
                    note.difficultyScore = (1.0 - pow(2, (-1.0 * score / 1000.0 + 0.84))) * 100.0
                else:
                    note.difficultyScore = score / 100.0
                modifiedNotes.append(note)

        notes.sort(key=lambda x: x.difficultyScore, reverse=True)

        logging.debug("Modified Notes " + str(len(modifiedNotes)))
        if len(modifiedNotes) > 0:
            return modifiedNotes

        return None