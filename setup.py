from distutils.core import setup

setup(
    name='pyark',
    version='0.5.0',
    packages=['pyark'],
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
