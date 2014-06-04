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
from zope.cachedescriptors.property import Lazy
from .queries import GroupUserEmailQuery
from .settings import GroupEmailSetting


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

    def set_digest(self):
        self.query.set_groupEmailSetting('digest')

    def set_webonly(self):
        self.query.set_groupEmailSetting('webonly')

    def set_default_delivery(self):
        self.query.clear_groupEmailSetting()
        for addr in self.get_specific_email_addresses():
            self.query.remove_groupUserEmail(addr)

    def add_specific_address(self, address):
        self.query.add_groupUserEmail(address)
