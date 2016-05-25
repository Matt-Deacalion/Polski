from setuptools import setup

import polski


setup(
    name='polski',
    version=polski.__version__.strip(),
    url='http://dirtymonkey.co.uk/polski',
    license='MIT',
    author=polski.__author__.strip(),
    author_email='matt@dirtymonkey.co.uk',
    description=polski.__doc__.strip().replace('\n', ' '),
    long_description=open('README.rst').read(),
    keywords='polski polish foreign language spaced repetition',
    packages=['polski'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'polski = polski.main:main',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
        'fuzzywuzzy>=0.10.0',
        'peewee>=2.8.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
)
