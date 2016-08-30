
import logging
import json

from core.service.lang.jp.JapaneseMorphemesService import JapaneseMorphemesService

from core.utils.utils import getList

class SiamorpheService:

    def __init__(self, language):

        logging.warning("ok siamorphe")

        if language == "jp":
            self.morphemesService = JapaneseMorphemesService()

    def createDataBase(self):

        logging.warning("create db")

    def analyzeExpressions(self, expressions):

        expressions = json.loads(expressions)

        allMorphemes = self.analyzeMorphemes(expressions)
        self.computeMorphemesScore(expressions, allMorphemes)

    def analyzeMorphemes(self, expressions):

        logging.debug("Extract Morphemes")
        allUniqueMorphemes = dict()
        for expression in expressions:
            expressionContent = expression["content"]
            logging.debug(expressionContent)

            morphemes = self.morphemesService.extractMorphemes(expressionContent)
            expressionMorphemes = set() # prevent duplicate morphemes in sentence
            for morpheme in morphemes:
                morphemeId = morpheme.id
                if morpheme in allUniqueMorphemes:
                    morpheme = allUniqueMorphemes[morphemeId]
                else:
                    allUniqueMorphemes[morphemeId] = morpheme
                expressionMorphemes.add(morpheme)
            expression["morphemes"] = expressionMorphemes

        allUniqueMorphemes = getList(allUniqueMorphemes)
        allUniqueMorphemes = self.morphemesService.filterMorphemes(allUniqueMorphemes)

        self.morphemesService.rankMorphemes(allUniqueMorphemes)

        #logging.debug(allUniqueMorphemes.get(0).score)
        #self.lemmeDao.persistLemmes(allUniqueMorphemes)

        return allUniqueMorphemes

    def computeMorphemesScore(self, expressions, allLemmes):

        for expression in expressions:
            morphemes = expression["morphemes"]
            for morpheme in morphemes:
                morpheme.score += expression["level"]

        logging.debug(expressions)


    def rankMorpheme(self, intervalDb, expr, read, rank):
        score = rank

        if read == None or rank == None:
            return 0

        if (expr, read) in intervalDb:
            interval = intervalDb[(expr, read)]
            score = score * self.getFactor(interval)
        else:
            hasKanji = False
            for i, c in enumerate(expr):
                # skip non-kanji
                if c < u'\u4E00' or c > u'\u9FBF': continue

                hasKanji = True
                npow = 0
                for (e,r), ivl in intervalDb.iteritems():
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