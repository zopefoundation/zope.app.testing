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

import io
NativeStringIO = io.BytesIO if str is bytes else io.StringIO

try:
    import mimetools
    headers_factory = mimetools.Message
except ImportError:
    # adapt Python 3 HTTP headers to old API
    from http import client # pylint:disable=import-error

    class OldMessage(client.HTTPMessage):
        def __init__(self, **kwargs):
            super(client.HTTPMessage, self).__init__(**kwargs) # pylint:disable=bad-super-call
            self.status = ''

        def getheader(self, name, default=None):
            return self.get(name, default)

        @property
        def headers(self):
            for key, value in self._headers:
                yield '%s: %s\r\n' % (key, value)

        @property
        def typeheader(self):
            return self.get('content-type')

    def headers_factory(fp): # pylint:disable=unused-argument
        try:
            ret = client.parse_headers(fp, _class=OldMessage)
        except client.LineTooLong:
            ret = OldMessage()
            ret.status = 'Line too long'
        return ret
