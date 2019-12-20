import os
from distutils.core import setup
from setuptools import find_packages
import pyark


test_deps = ['mock==3.0.5', 'pytest==4.6.4']

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))

setup(
    name='clinical-variant-ark',
    version=pyark.VERSION,
    description='A Python client for the Clinical Variant Ark',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/genomicsengland/pyark',
    download_url="https://github.com/genomicsengland/pyark/archive/v{}.tar.gz".format(pyark.VERSION),
    license='Apache',
    author=['Pablo Riesgo Ferreiro', 'Kevin Savage', 'William Bellamy'],
    author_email='pablo.riesgo-ferreiro@genomicsengland.co.uk',
    install_requires=[
        'requests==2.22.0',
        'furl==1.0.1',
        'gelreportmodels=100.0.0',
        'enum34==1.1.6',
        'pandas==0.24.2',
        'future==0.17.1'
    ],
    dependency_links=['git+https://github.com/genomicsengland/GelReportModels@develop#egg=gelreportmodels=100.0.0'],
    tests_require=test_deps,
    extras_require={'test': test_deps},
    keywords=['CVA', 'pyark', 'clinical variant ark', 'Genomics England'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ]
)
