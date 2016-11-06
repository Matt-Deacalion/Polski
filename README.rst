=============
Polski Runner
=============

A command line tool to teach myself Polish using a spaced repetition
algorithm.

Installation
------------
You can install *Polski Runner* using pip:

.. code-block:: bash

    $ pip install polski

Usage
-----
Use the `polski` command to run Polski Runner::

    $ polski --help

    Usage:
      polski [--insert | --report] [--database=<path>]
      polski (-h | --help | --version)

    Options:
      --version              show program's version number and exit.
      -h, --help             show this help message and exit.
      -i, --insert           insert new word iterations, starting from today.
      -r, --report           display a report of all daily iterations run.
      -d, --database=<path>  path to the SQLite database [default: db.sqlite3].

If no options are given, it will attempt to run through today's set
of words, if any exist. If there are none, it will go into insert
mode.

.. image:: https://raw.github.com/Matt-Deacalion/Polski/master/run-mode.gif
    :alt: Run Mode
    :align: center

.. image:: https://raw.github.com/Matt-Deacalion/Polski/master/input-mode.gif
    :alt: Insert Mode
    :align: center

License
-------
Copyright © 2016 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
