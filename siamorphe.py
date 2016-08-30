# -*- coding: utf-8 -*-

import json
import logging

from core.service.SiamorpheService import SiamorpheService

logging.basicConfig(level=logging.DEBUG)

expressions = """ [{"id": 1, "content": "日本語が大好きです", "score": 70},
                   {"id": 2, "content": "私が日本語を勉強しました", "score": 30},
                   {"id": 3, "content": "日本語の学校が第一", "score": 0}
                ] """

siamorpheService = SiamorpheService("jp")
siamorpheService.analyzeExpressions(expressions)