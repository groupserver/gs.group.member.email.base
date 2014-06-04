# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from enum import Enum


class GroupEmailSetting(Enum):
    '''An enumeration of the different group-email settings.'''
    __order__ = 'webonly default specific digest'  # only needed in 2.x

    #: The user follows the group using the web only (no email is sent).
    webonly = 0

    #: The user follows the group using his or her default email address
    #: settings.
    default = 1

    #: The user follows the group using an email address (or addresses) that is
    #: (or are) specific to this group
    specific = 2

    #: The user follows the group using a daily digest of topics
    digest = 3
