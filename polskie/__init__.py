"""
A command line tool to learn Polish using spaced repetition.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'


class Polskie:
    def __init__(self, **kwargs):
        self.report = kwargs.get('--report')
        self.insert = kwargs.get('--insert')
        self.db_path = kwargs.get('--database')

    def run(self):
        """
        Call to run Polskie.
        """
        print('Run...')
