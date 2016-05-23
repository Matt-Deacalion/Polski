from setuptools import setup

import polskie


setup(
    name='polskie',
    version=polskie.__version__.strip(),
    url='http://dirtymonkey.co.uk/polskie',
    license='MIT',
    author=polskie.__author__.strip(),
    author_email='matt@dirtymonkey.co.uk',
    description=polskie.__doc__.strip().replace('\n', ' '),
    long_description=open('README.rst').read(),
    keywords='polskie polish foreign language spaced repetition',
    packages=['polskie'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'polskie = polskie.main:main',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
)
