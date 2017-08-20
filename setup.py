#!/usr/bin/env python
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import bydict

setup(
    name='by',
    keywords=['dictionary', 'biying', 'word'],
    version=bydict.__version__,
    packages=['bydict'],
    url='https://github.com/louisun/iSearch',
    license='GPL3',
    author='spygg',
    author_email='liushidcn@163.com',
    description='比应词典单词查询、存储和管理的命令行工具',
    install_requires=[
        'pydub','bs4'
    ],
    entry_points = {
        'console_scripts': [
            'by = bydict.bydict:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
