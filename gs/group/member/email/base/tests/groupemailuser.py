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
from mock import MagicMock
from unittest import TestCase
from gs.profile.email.base.groupemailuser import (GroupEmailUser,
                                                    GroupEmailSetting)
import gs.profile.email.base.groupemailuser  # lint:ok


class FauxInfo(object):
    'Not a user'


class TestGroupEmailUser(TestCase):
    'Test the GroupEmailUser class'

    def setUp(self):
        self.fauxUser = FauxInfo()
        self.fauxUser.id = 'exampleUser'
        self.fauxGroup = FauxInfo()
        self.fauxGroup.id = 'exampleGroup'
        self.fauxGroup.siteInfo = FauxInfo()
        self.fauxGroup.siteInfo.id = 'exampleSite'

    def set_setting(self, setting):
        MockGUEQ = gs.profile.email.base.groupemailuser.GroupUserEmailQuery
        MockGUEQ.__init__ = MagicMock(return_value=None)
        MockGUEQ.get_groupEmailSetting = MagicMock(return_value=setting)
        return MockGUEQ

    def test_get_delivery_setting_webonly(self):
        'Test that a web-only setting works'
        MockGUEQ = self.set_setting('webonly')

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.webonly, r)

    def test_get_delivery_setting_digest(self):
        'Test that a digest setting works'
        MockGUEQ = self.set_setting('digest')

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.digest, r)

    def test_get_delivery_setting_default(self):
        'Test that the "default" delivery setting works'
        MockGUEQ = self.set_setting('asdfasdfasdf')
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=[])

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.default, r)

    def test_get_delivery_setting_specific(self):
        'Test that the group-specific delivery setting works.'
        MockGUEQ = self.set_setting('asdfasdfasdf')
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=['eg@example.com'])

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.specific, r)

    def test_get_addresses_webonly(self):
        'Test that get_addresses returns the default when it should'
        self.set_setting('webonly')
        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_addresses()
        self.assertEqual([], r)

    def test_get_addresses_specific(self):
        'Test that get_addresses returns the specific addresses when it should'
        MockGUEQ = self.set_setting('asdfasdf')
        specificAddresses = ['eg@example.com']
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=specificAddresses)

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_addresses()
        self.assertEqual(specificAddresses, r)

    def test_get_addresses_default(self):
        'Test that get_addresses returns the default addresses when it should'
        MockGUEQ = self.set_setting('asdfasdf')
        defaultAddresses = ['eg@example.com']
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=[])
        MockGUEQ.get_addresses = MagicMock(return_value=defaultAddresses)

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_addresses()
        self.assertEqual(defaultAddresses, r)
        MockGUEQ.get_addresses.assert_called_once_with(preferredOnly=True,
                                                        verifiedOnly=False)
