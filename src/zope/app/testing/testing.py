##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""zope.app.testing common test related classes/functions/objects.

"""

__docformat__ = "reStructuredText"

import os

import zope.publisher.interfaces.browser
from ZODB.POSException import ConflictError

from zope import component
from zope import interface
from zope.app.testing.functional import ZCMLLayer


AppTestingLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'AppTestingLayer', allow_teardown=True)


class IFailingKlass(interface.Interface):
    pass


@interface.implementer(IFailingKlass)
class FailingKlass:
    pass


@interface.implementer(zope.publisher.interfaces.browser.IBrowserPublisher)
@component.adapter(interface.Interface,
                   zope.publisher.interfaces.browser.IBrowserRequest)
class ConflictRaisingView:
    __used_for__ = IFailingKlass

    def __init__(self, context, request):
        pass

    def browserDefault(self, *_):
        return self, ()

    def __call__(self):
        raise ConflictError
