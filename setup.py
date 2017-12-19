##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.testing package


"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

TESTBROWSER_REQUIRES = [
    # zope.testbrowser version 5 has a new API and
    # doesn't have the 'connection' module
    'zope.testbrowser >=4,<5',
]

setup(name='zope.app.testing',
      version='3.11.0.dev0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Application Testing Support',
      long_description=(
          read('README.txt')
          + '\n\n.. contents::\n\n' +
          read('src', 'zope', 'app', 'testing', 'dochttp.txt')
          + '\n\n' +
          read('src', 'zope', 'app', 'testing', 'doctest.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords="zope3 test testing setup functional",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3',
      ],
      url="https://github.com/zopefoundation/zope.app.testing",
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require={
          'test': [
              'ZODB',
              'zope.app.zcmlfiles',
              'zope.login',
              'zope.publisher >= 3.12',
              'zope.securitypolicy',
              'zope.testrunner',
          ] + TESTBROWSER_REQUIRES,
          'testbrowser': TESTBROWSER_REQUIRES,
      },
      install_requires=[
          'setuptools',
          'zope.annotation',
          'zope.app.appsetup >= 3.11',
          'zope.processlifetime',
          'zope.app.debug',
          'zope.app.dependable',
          'zope.app.publication',
          # We need zope.component with the hooks module.
          'zope.component >= 3.8',
          'zope.container',
          'zope.i18n >= 4.3.0',
          'zope.interface',
          'zope.password',
          'zope.publisher',
          'zope.schema',
          'zope.security',
          'zope.site',
          'zope.testing',
          'zope.traversing',
      ],
      include_package_data=True,
      zip_safe=False,
)
