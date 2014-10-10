# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
from setuptools import setup, find_packages
import sys
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

requires = ['SQLAlchemy',
            'zope.cachedescriptors',
            'zope.component',  # For the ZCA, natch.
            'zope.interface',
            'zope.sqlalchemy',
            'gs.database', ]
if (sys.version_info < (3, 4)):
    requires += ['setuptools', 'enum34']

name = 'gs.group.member.email.base'

setup(name=name,
      version=version,
      description="The core group-member email code",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='user, group, member, group member, email',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://githhub.com/groupserver/{0}'.format(name),
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.group', 'gs.group.member',
                          'gs.group.member.email'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite='gs.group.member.email.base.test_all',
      tests_require=['mock'],
      entry_points="""
          # -*- Entry points: -*-
      """,)
