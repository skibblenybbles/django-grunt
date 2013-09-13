#!/usr/bin/env python

import os
from setuptools import setup, find_packages
import grunt


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as source:
        return source.read()


setup(
    name="django-grunt",
    version=grunt.__version__,
    description="Django tools for integrating Grunt into your workflow",
    long_description=read("README"),
    author="Mike Kibbel",
    author_email="mkibbel@gmail.com",
    url="https://github.com/skibblenybbles/django-grunt",
    license="MIT License",
    platforms=["OS Independent"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=[
        "Django>=1.4",
    ],
    packages=find_packages(exclude=["example", "example.*"]),
)
