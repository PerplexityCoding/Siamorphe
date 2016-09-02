
import logging
import json
import codecs
import os
import io

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

        self.saveNotesToJson(notes)

    def saveNotesToJson(self, notes):

        with io.open(os.getcwd() + "\\storage\\notes.json", "w", encoding='utf8') as outfile:
            outfile.write(u"[\n")
            i = 0
            for note in notes:
                note.morphemes = [m.id for m in note.morphemes]
                data = json.dumps(note, default=lambda o: o.__dict__, ensure_ascii=False, encoding='utf8')
                outfile.write(unicode(data)) # + u",\n"
                if (i + 1) < len(notes):
                    outfile.write(u",\n")
                i += 1

            outfile.write(u"]")

    def analyzeNotesFile(self, path):

        notes = self.loadNotesFromCsv(path)

        self.morphemesService.analyzeNotes(notes)

        self.saveNotesToJson(notes)

        #logging.debug(notes)

    def loadNotesFromCsv(self, path):

        notes = list()

        with codecs.open(path, "r", "utf-8") as row:
            for line in row:
                cells = line.rstrip().split("|")
                ivl = int(cells[2])

                notes.append(Note(cells[0], cells[1], (1.0 - pow(2, -1.0 * ivl / 24.0)) * 100.0))

        return notes

    def loadNotesFromJson(self, dict):
        return Note(dict["id"], dict["expression"], dict["level"])

