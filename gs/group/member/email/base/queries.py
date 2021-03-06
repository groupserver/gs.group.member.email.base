# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession


class GroupUserEmailQuery(object):
    possible_settings = ['webonly', 'digest']

    def __init__(self, userInfo, groupInfo):
        if not userInfo:
            raise ValueError('User info missing')
        if not groupInfo:
            raise ValueError('Group info missing')
        self.userId = userInfo.id
        self.groupId = groupInfo.id
        self.siteId = groupInfo.siteInfo.id
        self.emailSettingTable = getTable('email_setting')
        self.groupUserEmailTable = getTable('group_user_email')
        self.userEmailTable = getTable('user_email')

        assert self.userId, 'User ID not set'
        assert self.groupId, 'Group ID not set'
        assert self.siteId, 'Site ID not set'

    def add_groupUserEmail(self, email_address):
        uet = self.groupUserEmailTable
        i = uet.insert()
        d = {'user_id': self.userId,
             'site_id': self.siteId,
             'group_id': self.groupId,
             'email': email_address}

        session = getSession()
        session.execute(i, params=d)
        mark_changed(session)

    def remove_groupUserEmail(self, email_address):
        uet = self.groupUserEmailTable
        and_ = sa.and_
        e = email_address.lower()
        d = uet.delete(and_(uet.c.user_id == self.userId,
                            uet.c.site_id == self.siteId,
                            uet.c.group_id == self.groupId,
                            sa.func.lower(uet.c.email) == e))

        session = getSession()
        session.execute(d)
        mark_changed(session)

    def get_groupUserEmail(self, verified_only=True):
        guet = self.groupUserEmailTable
        s = guet.select()
        s.append_whereclause(guet.c.user_id == self.userId)
        s.append_whereclause(guet.c.site_id == self.siteId)
        s.append_whereclause(guet.c.group_id == self.groupId)
        if verified_only:
            uet = self.userEmailTable
            s.append_whereclause(uet.c.user_id == guet.c.user_id)
            s.append_whereclause(uet.c.verified_date != None)  # lint:ok

        session = getSession()
        r = session.execute(s)
        email_addresses = []
        for row in r.fetchall():
            email_address = row['email']
            if email_address not in email_addresses:
                email_addresses.append(email_address)

        return email_addresses

    def set_groupEmailSetting(self, setting):
        """ Given a site_id, group_id and a setting, set the email_setting
            table.
        """
        if setting not in self.possible_settings:
            raise ValueError("Unknown setting %s" % setting)
        est = self.emailSettingTable
        and_ = sa.and_
        curr_setting = self.get_groupEmailSetting()
        if not curr_setting:
            iOrU = est.insert()
            d = {'user_id': self.userId,
                 'site_id': self.siteId,
                 'group_id': self.groupId,
                 'setting': setting}

        else:
            iOrU = est.update(and_(est.c.user_id == self.userId,
                                   sa.or_(est.c.site_id == self.siteId,
                                          est.c.site_id == ''),
                                   est.c.group_id == self.groupId))
            d = {'setting': setting, }

        session = getSession()
        session.execute(iOrU, params=d)
        mark_changed(session)

    def clear_groupEmailSetting(self):
        est = self.emailSettingTable
        and_ = sa.and_

        d = est.delete(and_(est.c.user_id == self.userId,
                            sa.or_(est.c.site_id == self.siteId,
                                   est.c.site_id == ''),
                            est.c.group_id == self.groupId))

        session = getSession()
        session.execute(d)
        mark_changed(session)

    def get_groupEmailSetting(self):
        """ Given a site_id and group_id, check to see if the user
            has any specific email settings."""
        est = self.emailSettingTable
        s = est.select()
        s.append_whereclause(est.c.user_id == self.userId)
        # --=mpj17=-- Due to historical quirks, the site_id can be a bit
        # odd.
        s.append_whereclause(sa.or_(est.c.site_id == self.siteId,
                                    est.c.site_id == ''))
        s.append_whereclause(est.c.group_id == self.groupId)

        session = getSession()
        r = session.execute(s)
        setting = None
        if r.rowcount:
            result = r.fetchone()
            setting = result['setting']
        return setting

    def get_addresses(self, preferredOnly=False, verifiedOnly=True):
        # --=mpj17=-- Cut'n'paste software engineering. Forgive me.
        uet = self.userEmailTable
        s = sa.select([uet.c.email])
        s.append_whereclause(uet.c.user_id == self.userId)
        if preferredOnly:
            s.append_whereclause(uet.c.is_preferred == preferredOnly)
        if verifiedOnly:
            s.append_whereclause(uet.c.verified_date != None)  # lint:ok

        session = getSession()
        r = session.execute(s)

        retval = []
        for row in r.fetchall():
            retval.append(row['email'])
        return retval
