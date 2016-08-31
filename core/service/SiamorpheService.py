
import logging
import json

from core.service.lang.jp.JapaneseMorphemesService import JapaneseMorphemesService
from core.utils.utils import getList
from core.service.dto.Note import Note

class SiamorpheService:

    def __init__(self, language):

        logging.warning("ok siamorphe")

        if language == "jp":
            self.morphemesService = JapaneseMorphemesService()

    def analyzeNotes(self, notes):

        notes = json.loads(notes, object_hook=self.loadNotesFromJson)

        self.morphemesService.createNotesByKanji(notes)

        allMorphemes = self.analyzeMorphemes(notes)
        self.computeMorphemesScore(notes, allMorphemes)

    def loadNotesFromJson(self, dict):
        return Note(dict["id"], dict["expression"], dict["level"])

    def analyzeMorphemes(self, notes):

        logging.debug("Extract Morphemes")
        allUniqueMorphemes = dict()
        for note in notes:
            expression = note.expression
            logging.debug(expression)

            morphemes = self.morphemesService.extractMorphemes(expression)
            noteMorphemes = set() # prevent duplicate morphemes in sentence
            for morpheme in morphemes:
                morphemeId = morpheme.id
                if morpheme in allUniqueMorphemes:
                    morpheme = allUniqueMorphemes[morphemeId]
                else:
                    allUniqueMorphemes[morphemeId] = morpheme
                noteMorphemes.add(morpheme)
            note.morphemes = noteMorphemes

        allUniqueMorphemes = getList(allUniqueMorphemes)
        allUniqueMorphemes = self.morphemesService.filterMorphemes(allUniqueMorphemes)

        self.morphemesService.computeMorphemesBaseScore(allUniqueMorphemes)

        #logging.debug(allUniqueMorphemes.get(0).score)
        #self.lemmeDao.persistLemmes(allUniqueMorphemes)

        return allUniqueMorphemes

    def computeMorphemesScore(self, notes, allLemmes):

        for note in notes:
            morphemes = note.morphemes
            for morpheme in morphemes:
                morpheme.score += note.knowledgeLevel
                logging.debug(morpheme)

        logging.debug(notes)

    def computeNotesScore(self, notes):

        if notes == None:
            return None

        logging.debug("Compute Notes " + str(len(notes)))

        modifiedNotes = list()
        for note in notes:
            morphemes = note.morphemes
            score = 0
            for morpheme in morphemes:
                factor = pow(2, -1.0 * morpheme.score / 24.0) # number between 1 and 0; lim (itv -> +inf) -> 0
                score += 1000 * factor + morpheme.baseScore

            if note.score == 0 or note.score == None or abs(int(note.score) - int(score)) >= 15: #see if changing it every time is slow now
                note.score = score
                modifiedNotes.append(note)

        logging.debug("Modified Notes " + str(len(modifiedNotes)))
        if len(modifiedNotes) > 0:
            return modifiedNotes

        return None