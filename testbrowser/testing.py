##############################################################################
#
# Copyright (c) 2005 Zope Corporation. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Visible Source
# License, Version 1.0 (ZVSL).  A copy of the ZVSL should accompany this
# distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
import httplib
import urllib2
from cStringIO import StringIO

import mechanize
import ClientCookie

from zope.app.testing.functional import HTTPCaller


class PublisherConnection:

    def __init__(self, host):
        self.host = host
        self.caller = HTTPCaller()

    def set_debuglevel(self, level):
        pass

    def request(self, method, url, body=None, headers=None):
        header_chunks = []
        if body is None:
            body = ''

        if headers is not None:
            for header in headers.items():
                header_chunks.append('%s: %s' % header)
            headers = '\n'.join(header_chunks) + '\n'
        else:
            headers = ''

        request_string = (method + ' ' + url + ' HTTP/1.1\n'
                          + headers + '\n' + body)

        self.response = self.caller(request_string)

    def getresponse(self):
        headers = self.response.header_output.headersl
        real_response = self.response._response
        status = real_response.getStatus()
        reason = real_response._reason # XXX should add a getReason method
        output = (real_response.getHeaderText(real_response.getHeaders()) +
                  self.response.getBody())
        return PublisherResponse(output, status, reason)


class PublisherResponse:

    def __init__(self, content, status, reason):
        self.content = content
        self.status = status
        self.reason = reason
        self.msg = httplib.HTTPMessage(StringIO(content), 0)
        self.content_as_file = StringIO(content)

    def read(self, amt=None):
        return self.content_as_file.read(amt)


class PublisherHandler(urllib2.HTTPHandler):

    http_request = urllib2.AbstractHTTPHandler.do_request_

    def http_open(self, req):
        return self.do_open(PublisherConnection, req)


import browser

class MyMechBrowser(mechanize.Browser):
    handler_classes = {
        # scheme handlers
        "http": PublisherHandler,

        "_http_error": ClientCookie.HTTPErrorProcessor,
        "_http_request_upgrade": ClientCookie.HTTPRequestUpgradeProcessor,
        "_http_default_error": urllib2.HTTPDefaultErrorHandler,

        # feature handlers
        "_authen": urllib2.HTTPBasicAuthHandler,
        "_redirect": ClientCookie.HTTPRedirectHandler,
        "_cookies": ClientCookie.HTTPCookieProcessor,
        "_refresh": ClientCookie.HTTPRefreshProcessor,
        "_referer": mechanize.Browser.handler_classes['_referer'],
        "_equiv": ClientCookie.HTTPEquivProcessor,
        "_seek": ClientCookie.SeekableProcessor,
        }

    default_schemes = ["http"]
    default_others = ["_http_error", "_http_request_upgrade",
                      "_http_default_error"]
    default_features = ["_authen", "_redirect", "_cookies", "_seek"]


class Browser(browser.Browser):
    def __init__(self, url=None):
        mech_browser = MyMechBrowser()
        mech_browser.add_handler(PublisherHandler())
        super(Browser, self).__init__(url=url, mech_browser=mech_browser)
