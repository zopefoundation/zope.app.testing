##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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


from http import client


class OldMessage(client.HTTPMessage):
    def __init__(self, **kwargs):
        super(client.HTTPMessage, self).__init__(
            **kwargs)  # pylint:disable=bad-super-call
        self.status = ''

    @property
    def headers(self):
        for key, value in self._headers:
            yield f'{key}: {value}\r\n'


def headers_factory(fp):
    ret = client.parse_headers(fp, _class=OldMessage)
    return ret
