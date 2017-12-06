from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='brite-risktypes-model',
    version='0.1.0',
    packages=['brite.model'],
    author='Bruno Rezende',
    author_email='brunovianarezende@gmail.com',
    entry_points={
        'console_scripts': [
            'addnewtype=brite.model.command_line.add_new_type:add_new_type_main',
            'searchtypes=brite.model.command_line.search_types:search_types_main',
        ],
    },
      install_requires=required,
)
