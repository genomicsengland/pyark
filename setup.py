from distutils.core import setup
from setuptools import find_packages

test_deps = ['mock']

setup(
    name='pyark',
    version='2.0.2',
    packages=find_packages(),
    scripts=[],
    url='',
    license='',
    author='priesgo',
    author_email='pablo.ferreiro@genomicsengland.co.uk',
    description='',
    install_requires=[
        'requests',
        'furl==1.0.1',
        'gelreportmodels==7.1.12',
        'enum34',
        'pandas',
        'mock',
        'future'
    ],
    tests_require=test_deps,
    extras_require={'test': test_deps},
)
