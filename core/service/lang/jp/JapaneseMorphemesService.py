
import logging
from core.service.MorphemesService import *
from core.service.lang.jp.KanjiHelper import KanjiHelper
from core.service.ext.pos_tagger.Mecab import Mecab
from core.utils.utils import addItemInDictList

class JapaneseMorphemesService(MorphemesService):
    
    def __init__(self):
        MorphemesService.__init__(self)

        self.mecab = Mecab({})
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

                morpheme.baseScore += (self.computeKanjiScore(c) * 3)

            morpheme.baseScore = min(morpheme.baseScore, 500)

    # return a Score between 0 and 100
    def computeKanjiScore(self, kanji):
        kanjiScore = self.kanjisScoreCache.get(kanji)
        if kanjiScore:
            return kanjiScore

        kanjiFreq, kanjiStrokeCount = KanjiHelper.getKanjiInfo(kanji)
        
        freqScore =  pow(2, kanjiFreq / 900) * 7.0
        if freqScore > 70:
            freqScore = 70.0

        strokeScore = kanjiStrokeCount * 30.0 / 28.0
        if strokeScore > 30:
            strokeScore = 30.0

        kanjiScore = freqScore + strokeScore
        self.kanjisScoreCache[kanji] = kanjiScore

        return kanjiScore

    def createKanjiDicts(self, notes):
        notesByKanji = dict()
        morphemesByKanji = dict()

        for note in notes:
            for morpheme in note.morphemes:
                for i, c in enumerate(morpheme.base):
                    # skip non-kanji
                    if c < u'\u4E00' or c > u'\u9FBF': continue

                    addItemInDictList(notesByKanji, c, note.id)
                    addItemInDictList(morphemesByKanji, c, morpheme.id)

        self.notesByKanji = notesByKanji
        self.morphemesByKanji = morphemesByKanji

        logging.debug(notesByKanji)
        logging.debug(morphemesByKanji)

        return notesByKanji, morphemesByKanji

    def computeMorphemesScore(self, morphemes):

        logging.info("lemmeDao.getMorphemes() Start")
        if morphemes == None or len(morphemes) <= 0:
            return set()

        logging.info("Rank Morphemes Start: " + str(len(morphemes)))

        self.computeMorphemesBaseScore(morphemes)

        modifiedMorphemes = list()
        for morpheme in morphemes:
            score = self.computeMorphemeScore(morpheme)
            if morpheme.score == None or morpheme.score == 0 or abs(int(morpheme.score) - int(score)) >= 5:
                morpheme.score = score
                modifiedMorphemes.append(morpheme)

                logging.debug(morpheme)

    # Adapted from MorphMan 2
    def computeMorphemeScore(self, morpheme):
        score = morpheme.baseScore
        expr = morpheme.base
        read = morpheme.read
        knowledgeLevel = morpheme.knowledgeLevel / 100.0

        if knowledgeLevel == 0:
            return 500 + min(score, 500)

        if read == None or score == None:
            return 0

        if knowledgeLevel > 0:
            score = score * (1.0 - knowledgeLevel)
        else:
            for i, c in enumerate(expr):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue

                morphemesId = self.morphemesByKanji[c]

                npow = 0
                if morphemesId != None:
                    for morphemeId in morphemesId:
                        morpheme = self.morphemesById[morphemeId]
                        if morpheme != None:
                            e = morpheme.base
                            r = morpheme.read
                            ivl = morpheme.knowledgeLevel

                            # has same kanji
                            if c in e:
                                if npow > -1.0: npow -= 0.25
                                # has same kanji at same pos
                                if len(e) > i and c == e[i]:
                                    if npow > -1.5: npow -= 0.2
                                    # has same kanji at same pos with similar reading
                                    if i == 0 and read[0] == r[0] or i == len(expr)-1 and read[-1] == r[-1]:
                                        npow -= 1.0
                                npow = npow * knowledgeLevel
                score *= pow(2, npow)
        return min(score, 1000)

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