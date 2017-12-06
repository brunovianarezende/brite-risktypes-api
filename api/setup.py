from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='brite-risktypes-api',
    version='0.1.0',
    packages=['brite.api'],
    author='Bruno Rezende',
    author_email='brunovianarezende@gmail.com',
    install_requires=required,
)
