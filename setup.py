"""
Python package configuration.
"""

from setuptools import setup

setup(
    name='wolfpack',
    version='0.1.0',
    packages=['wolfpack'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'nodeenv',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
    ],
    python_requires='>=3.6',
)
