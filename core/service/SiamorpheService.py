
import logging
import json

from core.service.lang.jp.JapaneseMorphemesService import JapaneseMorphemesService
from core.service.dto.Note import Note

class SiamorpheService:

    def __init__(self, language):

        logging.warning("ok siamorphe")

        if language == "jp":
            self.morphemesService = JapaneseMorphemesService()

    def analyzeNotes(self, notes):

        notes = json.loads(notes, object_hook=self.loadNotesFromJson)

        self.morphemesService.analyzeNotes(notes)

        logging.debug(notes)

    def loadNotesFromJson(self, dict):
        return Note(dict["id"], dict["expression"], dict["level"])

