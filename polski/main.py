# coding=utf-8

"""Usage:
  polski [--insert | --report] [--database=<path>]
  polski (-h | --help | --version)

Options:
  --version              show program's version number and exit.
  -h, --help             show this help message and exit.
  -i, --insert           insert new word iterations, starting from today.
  -r, --report           display a report of all daily iterations run.
  -d, --database=<path>  path to the SQLite database [default: db.sqlite3].
"""
from datetime import date, datetime, timedelta

from docopt import docopt

from fuzzywuzzy import fuzz
from peewee import (CharField, DateField, DateTimeField, ForeignKeyField,
                    IntegrityError, Model, SqliteDatabase)
from polski import __version__

database = SqliteDatabase(None)


class Polski:
    def __init__(self, **kwargs):
        self.report = kwargs.get('--report')
        self.insert = kwargs.get('--insert')
        self.db_path = kwargs.get('--database')

    def run(self):
        """
        Call this to run Polski.
        """
        self._start_db()

        if self.insert:
            self.insert_mode()
        else:
            words = Word.get_day_iterations()

            if not words:
                print('No words in database. Gone into insert mode.')
                self.insert_mode()
            else:
                self.run_mode(words)

        self._end_db()

    def run_mode(self, words):
        """
        Go through `words` and ask for their English definitions.
        """
        # ANSI codes to move the cursor and make the tick green
        tick = '\033[32m\033[{}C\033[1A ✓\033[39m'

        for word in words:
            prompt = '{} > '.format(word.word)
            correct = False

            while not correct:
                translation = input(prompt)
                correct = word.check_translation(translation)

                if correct:
                    print(tick.format(len(prompt + translation)))

        Run.create()

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

    @classmethod
    def get_day_iterations(cls, day=None):
        """
        Takes an optional `date` object and returns all the words to
        be iterated for that day.
        """
        if day is None:
            day = date.today()

        return Word.select().join(Iteration).where(
            Iteration.date == day,
        ).group_by(Word)

    def check_translation(self, translation):
        """
        Takes a `translation` and returns `True` if it's correct.
        """
        return any(
            fuzz.token_sort_ratio(translation, t.translation) >= 90
            for t in self.translations
        )


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
    A completed `Run` of an `Iteration`.
    """
    date = DateTimeField(default=datetime.now)


def main():
    """
    The entry point for the Polski command line tool.
    """
    Polski(**docopt(__doc__, version=__version__)).run()

if __name__ == '__main__':
    main()
