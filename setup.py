from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='pytabcmd',
    version='9.2.0',
    description='A tabcmd wrapper for Python',
    author='MiguelSR',
    author_email='miguelsr87@gmail.com',
    packages=find_packages(exclude=['tests']),
    keywords='tabcmb tableau',
    url='https://github.com/AccesoGroup/pytabcmd'
)
