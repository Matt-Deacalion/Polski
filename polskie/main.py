# coding=utf-8

"""Usage:
  polskie [--insert | --report] [--database=<path>]
  polskie (-h | --help | --version)

Options:
  --version              show program's version number and exit.
  -h, --help             show this help message and exit.
  -i, --insert           insert new word iterations, starting from today.
  -r, --report           display a report of all daily iterations run.
  -d, --database=<path>  path to the SQLite database [default: db.sqlite3].
"""
from docopt import docopt

from polskie import Polskie, __version__


def main():
    """
    The entry point for the Polskie command line tool.
    """
    Polskie(**docopt(__doc__, version=__version__)).run()

if __name__ == '__main__':
    main()
