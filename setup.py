from distutils.core import setup
from setuptools import find_packages
import pyark

test_deps = ['mock']

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
        'requests',
        'furl==1.0.1',
        'gelreportmodels==7.2.10',
        'enum34',
        'pandas',
        'mock',
        'future',
        'pytest'
    ],
    tests_require=test_deps,
    extras_require={'test': test_deps},
    keywords=['CVA', 'pyark', 'clinical variant ark', 'Genomics England']
)
