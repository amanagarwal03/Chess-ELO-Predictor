__author__ = 'Mayank Tiwari'

import datetime

from mongoengine import *


class Metadata(EmbeddedDocument):
    sequenceNumber = IntField()
    sourceFileName = StringField(required=True)
    CreateDate = DateTimeField(default=datetime.datetime.now)
    LastUpdateDate = DateTimeField(default=datetime.datetime.now)

    def __init__(self, sequenceNumber: int, sourceFileName: str, *args, **values):
        super().__init__(*args, **values)
        self.sequenceNumber = sequenceNumber
        self.sourceFileName = sourceFileName


class Move(EmbeddedDocument):
    gameId = ReferenceField('Game')
    uci = StringField(required=True)
    fen = StringField(required=True)
    encodedMove = StringField(required=True)
    score = IntField(default=0)  # DecimalField
    previousMoveScore = IntField(default=0)
    turn = BooleanField(required=True)
    isMate = BooleanField(default=False)

    # CreateDate = DateTimeField()
    # LastUpdateDate = DateTimeField(default=datetime.datetime.now)

    def __init__(self, uci: str, fen: str, encodedMove: str, score: str, previousMoveScore: str, turn: bool, isMate=False, *args, **values):
        super().__init__(*args, **values)
        self.uci = uci
        self.fen = fen
        self.encodedMove = encodedMove
        self.score = score
        self.previousMoveScore = previousMoveScore
        self.turn = turn
        self.isMate = isMate


class Game(Document):
    event = StringField(required=True)
    site = StringField(required=True)
    white = StringField(required=True)
    black = StringField(required=True)
    result = StringField(required=True)
    uTCDate = StringField(required=True)
    uTCTime = StringField(required=True)
    whiteElo = StringField(required=True)
    blackElo = StringField(required=True)
    whiteRatingDiff = StringField()
    blackRatingDiff = StringField()
    eCO = StringField(required=True)
    opening = StringField(required=True)
    timeControl = StringField(required=True)
    termination = StringField(required=True)
    # moves = ListField(ReferenceField(Move))
    metadata = EmbeddedDocumentField(Metadata)
    moves = ListField(EmbeddedDocumentField(Move))

    def __init__(self, headers=None, metadata=None, *args, **values):
        super().__init__(*args, **values)
        if headers is not None:
            self.event = headers.get("Event")
            self.site = headers.get("Site")
            self.white = headers.get("White")
            self.black = headers.get("Black")
            self.result = headers.get("Result")
            self.uTCDate = headers.get("UTCDate")
            self.uTCTime = headers.get("UTCTime")
            self.whiteElo = headers.get("WhiteElo")
            self.blackElo = headers.get("BlackElo")
            self.whiteRatingDiff = headers.get("WhiteRatingDiff")
            self.blackRatingDiff = headers.get("BlackRatingDiff")
            self.eCO = headers.get("ECO")
            self.opening = headers.get("Opening")
            self.timeControl = headers.get("TimeControl")
            self.termination = headers.get("Termination")
            self.metadata = metadata
            self.moves = []

    def site_exists(site_id) -> bool:
        return Game.objects(site=site_id).count() != 0
