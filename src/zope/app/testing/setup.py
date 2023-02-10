##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Setting up an environment for testing context-dependent objects

"""
import sys

import zope.component
import zope.component.hooks
import zope.component.interfaces
import zope.traversing.api
# ------------------------------------------------------------------------
# Annotations
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.dependable import Dependable
from zope.app.dependable.interfaces import IDependable
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
from zope.interface import Interface
from zope.interface.interfaces import IComponentLookup
from zope.site.folder import Folder
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager
from zope.site.site import SiteManagerAdapter
from zope.testing.module import FakeModule
from zope.traversing.interfaces import ITraversable

from zope.app.testing.placelesssetup import setUp as placelessSetUp
from zope.app.testing.placelesssetup import tearDown as placelessTearDown


def setUpAnnotations():
    zope.component.provideAdapter(AttributeAnnotations)


# ------------------------------------------------------------------------
# Dependencies


def setUpDependable():
    zope.component.provideAdapter(Dependable, (IAttributeAnnotatable,),
                                  IDependable)


# ------------------------------------------------------------------------
# Traversal


def setUpTraversal():
    from zope.traversing.testing import setUp
    setUp()
    zope.component.provideAdapter(ContainerTraversable,
                                  (ISimpleReadContainer,), ITraversable)


# ------------------------------------------------------------------------
# ISiteManager lookup


def setUpSiteManagerLookup():
    zope.component.provideAdapter(SiteManagerAdapter, (Interface,),
                                  IComponentLookup)


# ------------------------------------------------------------------------
# Placeful setup


def placefulSetUp(site=False):
    placelessSetUp()
    zope.component.hooks.setHooks()
    setUpAnnotations()
    setUpDependable()
    setUpTraversal()
    setUpSiteManagerLookup()

    if site:
        site = rootFolder()
        createSiteManager(site, setsite=True)
        return site


def placefulTearDown():
    placelessTearDown()
    zope.component.hooks.resetHooks()
    zope.component.hooks.setSite()


# ------------------------------------------------------------------------
# Sample Folder Creation


def buildSampleFolderTree():
    # set up a reasonably complex folder structure
    #
    #     ____________ rootFolder ______________________________
    #    /                                    \                 \
    # folder1 __________________            folder2           folder3
    #   |                       \             |                 |
    # folder1_1 ____           folder1_2    folder2_1         folder3_1
    #   |           \            |            |
    # folder1_1_1 folder1_1_2  folder1_2_1  folder2_1_1

    root = rootFolder()
    root['folder1'] = Folder()
    root['folder1']['folder1_1'] = Folder()
    root['folder1']['folder1_1']['folder1_1_1'] = Folder()
    root['folder1']['folder1_1']['folder1_1_2'] = Folder()
    root['folder1']['folder1_2'] = Folder()
    root['folder1']['folder1_2']['folder1_2_1'] = Folder()
    root['folder2'] = Folder()
    root['folder2']['folder2_1'] = Folder()
    root['folder2']['folder2_1']['folder2_1_1'] = Folder()
    root["\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER A}"
         "\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER KA}"
         "\N{CYRILLIC SMALL LETTER A}3"] = Folder()
    root["\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER A}"
         "\N{CYRILLIC SMALL LETTER PE}"
         "\N{CYRILLIC SMALL LETTER KA}"
         "\N{CYRILLIC SMALL LETTER A}3"][
        "\N{CYRILLIC SMALL LETTER PE}"
        "\N{CYRILLIC SMALL LETTER A}"
        "\N{CYRILLIC SMALL LETTER PE}"
        "\N{CYRILLIC SMALL LETTER KA}"
        "\N{CYRILLIC SMALL LETTER A}3_1"] = Folder()

    return root


# ------------------------------------------------------------------------
# Sample Folder Creation


def createSiteManager(folder, setsite=False):
    if not zope.component.interfaces.ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        zope.component.hooks.setSite(folder)
    return zope.traversing.api.traverse(folder, "++etc++site")


# ------------------------------------------------------------------------
# Local Utility Addition
def addUtility(sitemanager, name, iface, utility, suffix=''):
    """Add a utility to a site manager

    This helper function is useful for tests that need to set up utilities.
    """
    folder_name = (name or (iface.__name__ + 'Utility')) + suffix
    default = sitemanager['default']
    default[folder_name] = utility
    utility = default[folder_name]
    sitemanager.registerUtility(utility, iface, name)
    return utility


# ------------------------------------------------------------------------
# Setup of test text files as modules

# Evil hack to make pickling work with classes defined in doc tests

class NoCopyDict(dict):
    def copy(self):
        return self


def setUpTestAsModule(test, name=None):
    if name is None:
        if '__name__' in test.globs:
            name = test.globs['__name__']
        else:
            name = test.globs.name

    test.globs['__name__'] = name
    test.globs = NoCopyDict(test.globs)
    sys.modules[name] = FakeModule(test.globs)


def tearDownTestAsModule(test):
    del sys.modules[test.globs['__name__']]
    test.globs.clear()
