
import logging
from core.service.MorphemesService import *
from core.service.lang.jp.KanjiHelper import KanjiHelper
from core.service.ext.pos_tagger.Mecab import Mecab

class JapaneseMorphemesService(MorphemesService):
    
    def __init__(self):
        MorphemesService.__init__(self)

        self.mecab = Mecab({})
        self.initFactors()
        self.kanjisScoreCache = dict()

    def extractMorphemes(self, expression):
        morphemes = self.mecab.posMorphemes(expression)
        return morphemes

    def computeMorphemesBaseScore(self, morphemes):

        logging.info("rankMorphemes")
        for morpheme in morphemes:

            base = morpheme.base
            morpheme.baseScore = len(base) * 10

            for i,c in enumerate(base):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue

                morpheme.baseScore += self.computeKanjiScore(c)

    # return a Rank between 0 and 500
    def computeKanjiScore(self, kanji):
        kanjiScore = self.kanjisScoreCache.get(kanji)
        if kanjiScore:
            return kanjiScore

        kanjiFreq, kanjiStrokeCount = KanjiHelper.getKanjiInfo(kanji)
        
        freqScore =  pow(2, kanjiFreq / 900) * 35.0
        if freqScore > 350:
            freqScore = 350.0

        strokeScore = kanjiStrokeCount * 150.0 / 28.0
        if strokeScore > 150:
            strokeScore = 150.0

        kanjiScore = freqScore + strokeScore
        self.kanjisScoreCache[kanji] = kanjiScore

        return kanjiScore

    def createNotesByKanjiDict(self, notes):
        notesByKanji = dict()

        for note in notes:
            for i, c in enumerate(note.expression):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue

                notesByKanjiList = notesByKanji.get(c)
                if notesByKanjiList == None:
                    notesByKanjiList = list()
                    notesByKanji[c] = notesByKanjiList

                notesByKanjiList.append(note.id)

        logging.debug(notesByKanji)
        return notesByKanji

    def computeMorphemesScore(self, morphemes):

        logging.info("lemmeDao.getMorphemes() Start")
        if morphemes == None or len(morphemes) <= 0:
            return set()

        logging.info("Rank Morphemes Start: " + str(len(morphemes)))

        #intervalDb = self.lemmeDao.getKnownLemmesIntervalDB()

        morphemesKnowledgeDB = {}

        modifiedMorphemes = list()
        for morpheme in morphemes:
            score = self.computeMorphemeScore(morpheme, morphemesKnowledgeDB)
            if morpheme.score == None or morpheme.score == 0 or abs(int(morpheme.score) - int(score)) >= 5:
                morpheme.score = score
                modifiedMorphemes.append(morpheme)

        logging.info("Update all Score " + str(len(modifiedLemmes)))
        if len(modifiedLemmes) > 0:
            self.lemmeDao.updateLemmesScore(modifiedLemmes)

            logging.info("Mark Modified Notes: " + str(len(modifiedLemmes)))
            notes = self.morphemeDao.getModifiedNotes(modifiedLemmes)
            logging.info("getModifiedNotes() : " + str(len(modifiedLemmes)))
            return notes

        return set()

    # Adapted from MorphMan 2
    def computeMorphemeScore(self, morpheme, morphemesById):
        score = morpheme.baseScore
        expr = morpheme.base
        read = morpheme.read

        if read == None or score == None:
            return 0

        if morpheme.id in morphemesById:
            morphemesKnowledgeLevel = morphemesById[morpheme.id]
            score = score * self.getFactor(morphemesKnowledgeLevel)
        else:
            for i, c in enumerate(expr):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue
                
                npow = 0
                for morpheme, ivl in morphemesKnowledgeDB.iteritems():
                    e = morpheme.base
                    r = morpheme.read

                    # has same kanji
                    if c in e:
                        if npow > -1.0: npow -= 0.25
                        # has same kanji at same pos
                        if len(e) > i and c == e[i]:
                            if npow > -1.5: npow -= 0.2
                            # has same kanji at same pos with similar reading
                            if i == 0 and read[0] == r[0] or i == len(expr)-1 and read[-1] == r[-1]:
                                npow -= 1.0
                        npow = npow * (1.0 - self.getFactor(ivl))
                score *= pow(2, npow)
        return score

    def initFactors(self):
        self.cachePow = dict()
        for i in range(1000):
            self.cachePow[i] = pow(2, -1.0 * i / 24.0)

    def getFactor(self, interval):
        return self.cachePow[interval]
    
    def getLinkedMorphemes(self, allLemmes):
        if len(allLemmes) <= 0:
            return set()
        
        kanjis = set()
        for lemme in allLemmes:
            expr = lemme.base
            for i, c in enumerate(expr):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue
                kanjis.add(c)

        if len(kanjis) < 0:
            return allLemmes
        return self.lemmeDao.getChangedAllMorphemesFromKanjis(kanjis)
    
    def filterMorphemes(self, morphemes):
        # Do nothing
        return morphemes