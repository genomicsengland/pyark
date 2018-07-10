from distutils.core import setup
from setuptools import find_packages

setup(
    name='pyark',
    version='0.3.0',
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
        'gelreportmodels==7.0.4',
        'enum34',
        'pandas'
    ]
)
