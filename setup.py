#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Sid.
# https://github.com/yoavram/Sid

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>

from setuptools import setup, find_packages
import os
import versioneer

README = """Python script for image processing of plant seed images, specifically *Lamium amplexicaule*.

See https://github.com/yoavram/Sid.
"""

setup(
    name='Sid',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Image processing for seed images',
    long_description=README,
    keywords='biology image-processing plant-science',
    author='Yoav Ram',
    author_email='yoav@yoavram.com',
    url='https://github.com/yoavram/Sid',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'Sid.images': [
            'image1.jpg', 
            'image2.jpg', 
            'image3.jpg'
        ],
        'Sid': [
            'take_cover.json'
        ],
    },    
    install_requires=[
    # add your dependencies here
    # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-image',
        'pillow',
        'watchdog',
        'click',
        'colorama',
        'scikit-image'
    ],
    extras_require={
        # https://www.python.org/dev/peps/pep-0426/#environment-markers
        ':sys_platform == "win32"': [
            'pypiwin32'
        ],
        'tests': [
            'nose',
            'coverage',
        ],
        'docs': [
            'sphinx>=1.3.0'
        ]
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'take_cover=Sid.take_cover:main',
        ],
    },
)
