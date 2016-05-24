"""
A command line tool to learn Polish using spaced repetition.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'

from datetime import datetime

from peewee import (CharField, DateField, DateTimeField, ForeignKeyField,
                    Model, SqliteDatabase)

database = SqliteDatabase(None)


class Polskie:
    def __init__(self, **kwargs):
        self.report = kwargs.get('--report')
        self.insert = kwargs.get('--insert')
        self.db_path = kwargs.get('--database')

    def run(self):
        """
        Call this to run Polskie.
        """
        self._start_db()
        self._end_db()

    def _start_db(self):
        """
        Initialise the database, connect to it and create the tables.
        """
        database.init(self.db_path)
        database.connect()
        database.create_tables(
            [Word, Iteration, Translation, Run],
            safe=True,  # fail silently if our tables already exist
        )

    def _end_db(self):
        """
        Close the database connection.
        """
        database.close()


class BaseModel(Model):
    class Meta:
        database = database


class Word(BaseModel):
    """
    A Polish word along with it's phonetic pronunciation in English.
    """
    word = CharField(unique=True)
    pronunciation = CharField(null=True)


class Iteration(BaseModel):
    """
    An entity to store which `Words` should be revised and when.
    """
    word = ForeignKeyField(Word, related_name='iterations')
    date = DateField()


class Translation(BaseModel):
    """
    A single translation from Polish to English.
    """
    word = ForeignKeyField(Word, related_name='translations')
    translation = CharField()


class Run(BaseModel):
    """
    A completed `run` of an `Iteration`.
    """
    date = DateTimeField(default=datetime.now)
