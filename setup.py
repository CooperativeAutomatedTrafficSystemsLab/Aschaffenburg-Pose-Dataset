# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Aschaffenburg_Pose_Dataset',
    version='1.0',
    description='Tools for loading and filtering the Aschaffenburg Pose Dataset',
    long_description=readme,
    author='Viktor Kress',
    author_email='viktor.kress@gmx.net',
    url='https://github.com/CooperativeAutomatedTrafficSystemsLab/Aschaffenburg-Pose-Dataset',
    license=license,
    packages=find_packages(exclude=('examples'))
)
