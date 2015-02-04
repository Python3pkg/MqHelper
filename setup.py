#!/usr/bin/env python

from distutils.core import setup

execfile('package/MqHelper.py')

setup(name='MqHelper',
      version='1.0',
      description='Message-Queue Helper for Mosquitto',
      author='Paul Klingelhuber',
      author_email='paul@paukl.at',
      url='http://www.paukl.at/',
      package_dir = {'': 'package'},
      py_modules = ['MqHelper']
     )