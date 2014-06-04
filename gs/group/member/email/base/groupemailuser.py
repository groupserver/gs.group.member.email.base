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
from zope.cachedescriptors.property import Lazy
from .queries import GroupUserEmailQuery


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


class GroupEmailUser(object):
    '''A user of email in a group

:param UserInfo userInfo: The info-object for the group member.
:param GroupInfo groupInfo: The info-object for the group.'''

    def __init__(self, userInfo, groupInfo):
        self.userInfo = userInfo
        self.groupInfo = groupInfo

    @Lazy
    def query(self):
        retval = GroupUserEmailQuery(self.userInfo, self.groupInfo)
        return retval

    def get_delivery_setting(self):
        '''Get the message delivery settings for a user in a group.

:returns: The delivery settings for a user.
:rtype: A member of :class:`GroupEmailSetting`.'''
        setting = self.query.get_groupEmailSetting()
        if setting == 'webonly':
            retval = GroupEmailSetting.webonly
        elif setting == 'digest':
            retval = GroupEmailSetting.digest
        elif self.get_specific_email_addresses():
            retval = GroupEmailSetting.specific
        else:
            retval = GroupEmailSetting.default
        return retval

    def get_addresses(self):
        """ Get the user's preferred delivery email address. If none is
        set, it defaults to the first in the list."""
        retval = []

        # First, check to see if we are not web only
        groupSetting = self.get_delivery_setting()
        if groupSetting != GroupEmailSetting.webonly:
            # Next, check to see if we've customised the delivery options
            #   for that group
            # TODO: Check email addr
            retval = self.get_specific_email_addresses()
            if not retval:
                # If there are no specific settings for the group, return
                #   the default settings
                retval = self.get_preferred_email_addresses()
        return retval

    def get_specific_email_addresses(self):
        '''Get the specific email addresses for a member of a group

:returns: A list of email addresses that the current user has set for
          specific delivery. If no addresses are set an empty list is
          returned.
:rtype: ``list``'''
        retval = self.query.get_groupUserEmail()
        return retval

    def get_preferred_email_addresses(self):
        'Get the preferred email addresses of a group member.'
        retval = self.query.get_addresses(preferredOnly=True,
                                            verifiedOnly=False)
        return retval
