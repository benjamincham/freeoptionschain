from setuptools import setup, Extension
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='freeoptionschain',
    
    version='{{VERSION_PLACEHOLDER}}',

    description='This library module retrieves stock options data from NASDAQ.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/benjamincham/free_options_chain',

    author='Benjamin Cham',

    author_email='benjaminchamwb@gmail.com',

    classifiers=[
        'Topic :: Office/Business :: Financial :: Investment',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    packages=['FOC'],
    
    install_requires=[
        'requests',
        'pandas',
        'yfinance',
        'yahoo_fin',
        'pytz',
        'urllib3',
        'build',
    ],
    setup_requires=[
        'build',
    ],
    python_requires='>=3.6, <4',

)