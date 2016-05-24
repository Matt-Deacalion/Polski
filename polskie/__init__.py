"""
A command line tool to learn Polish using spaced repetition.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'

from datetime import date, datetime, timedelta

from peewee import (CharField, DateField, DateTimeField, ForeignKeyField,
                    IntegrityError, Model, SqliteDatabase)

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
        self.insert_mode()
        self._end_db()

    def insert_mode(self):
        """
        Takes user input and uses it to populate the database.
        """
        words_saved_count = 0

        while True:
            input_word = input('Polish word: ').strip().lower()

            if not input_word:
                break

            try:
                word = Word.create(word=input_word)
            except IntegrityError:
                print('"{}" already exists'.format(input_word))
                continue

            self.get_pronunciation(word)
            self.get_translations(word)

            words_saved_count += 1

        if words_saved_count == 0:
            print('No words added.')
        else:
            print('{} word{} saved.'.format(
                words_saved_count,
                's'[words_saved_count == 1:],
            ))

    def get_pronunciation(self, word):
        """
        Takes a `word` instance, asks the user for the corresponding
        pronunciation and adds it to the `word`.
        """
        pronunciation = ''

        while not pronunciation:
            pronunciation = input('Pronunciation: ')

        word.pronunciation = pronunciation.strip().lower()
        word.save()

    def get_translations(self, word):
        """
        Asks and creates one or more translations for a word.
        """
        translations_count = 0

        while True:
            translation = input('Translation: ')

            if not translation:
                if translations_count == 0:
                    continue
                else:
                    break

            Translation.create(
                word=word,
                translation=translation.strip().lower(),
            )
            translations_count += 1

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

    def save(self, *args, **kwargs):
        """
        This has been overriden to automatically create the related
        `Iteration` instances upon saving.
        """
        is_new = self.id is None

        super().save(*args, **kwargs)

        if is_new:
            dates = [date.today() + timedelta(i) for i in [
                1, 3, 5, 8, 13, 19, 25, 35,
            ]]

            for interval_date in dates:
                Iteration.create(word=self, date=interval_date)


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
