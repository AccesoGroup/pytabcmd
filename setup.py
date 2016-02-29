from setuptools import setup, find_packages

setup(
    name='pytabcmd',
    version='9.2.0',
    description='A tabcmd wrapper for Python',
    url='https://github.com/AccesoGroup/pytabcmd',
    author='MiguelSR',
    author_email='miguelsr87@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    keywords='tabcmb tableau',
    install_requires=['configparser']
)
