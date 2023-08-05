from setuptools import setup, Extension
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='freeoptionschain',

    description='This downloads stock option data and calculates its greeks.',

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
    
    package_data={'FOC': ['db.cpython-38-x86_64-linux-gnu.so']},

    install_requires=[
        'requests',
        'pandas',
        'yfinance',
        'yahoo_fin',
        'pytz',
        'urllib3',
        'build',
        'cython',
    ],
    setup_requires=[
        'build',
        'cython',
    ],
    python_requires='>=3.6, <4',

)