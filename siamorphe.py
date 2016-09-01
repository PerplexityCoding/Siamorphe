# -*- coding: utf-8 -*-

import json
import logging

from core.service.SiamorpheService import SiamorpheService

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

notes = """ [{"id": 1, "expression": "日本語が大好きです", "level": 70},
             {"id": 2, "expression": "私が日本語を勉強しました", "level": 30},
             {"id": 3, "expression": "日本語の学校が第一", "level": 0}
             ] """

siamorpheService = SiamorpheService("jp")
#siamorpheService.analyzeNotes(notes)
siamorpheService.analyzeNotesFile('C://Users//yves_menard//Perso//Workspace//Siamorphe//sample//notes2.csv')