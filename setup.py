##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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

$Id$
"""

import zope.component
import zope.interface
from zope.app import zapi
from zope.app.testing import ztapi
from zope.interface import classImplements

#------------------------------------------------------------------------
# Annotations
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.annotation.interfaces import IAnnotations
from zope.app.annotation.interfaces import IAttributeAnnotatable
def setUpAnnotations():
    ztapi.provideAdapter(IAttributeAnnotatable, IAnnotations,
                         AttributeAnnotations)

#------------------------------------------------------------------------
# Dependencies
from zope.app.dependable import Dependable
from zope.app.dependable.interfaces import IDependable
def setUpDependable():
    ztapi.provideAdapter(IAttributeAnnotatable, IDependable,
                         Dependable)

#------------------------------------------------------------------------
# Traversal
from zope.app.traversing.browser.interfaces import IAbsoluteURL
from zope.app.container.traversal import ContainerTraversable
from zope.app.container.interfaces import ISimpleReadContainer
from zope.app.traversing.interfaces import IContainmentRoot
from zope.app.traversing.interfaces import IPhysicallyLocatable
from zope.app.traversing.interfaces import ITraverser, ITraversable
from zope.app.traversing.adapters import DefaultTraversable
from zope.app.traversing.adapters import Traverser, RootPhysicallyLocatable
from zope.app.location.traversing import LocationPhysicallyLocatable
from zope.app.traversing.namespace import etc

def setUpTraversal():
    from zope.app.traversing.browser import SiteAbsoluteURL, AbsoluteURL

    ztapi.provideAdapter(None, ITraverser, Traverser)
    ztapi.provideAdapter(None, ITraversable, DefaultTraversable)

    ztapi.provideAdapter(
        ISimpleReadContainer, ITraversable, ContainerTraversable)
    ztapi.provideAdapter(
        None, IPhysicallyLocatable, LocationPhysicallyLocatable)
    ztapi.provideAdapter(
        IContainmentRoot, IPhysicallyLocatable, RootPhysicallyLocatable)

    # set up etc namespace
    ztapi.provideAdapter(None, ITraversable, etc, name="etc")
    ztapi.provideView(None, None, ITraversable, "etc", etc)

    ztapi.browserView(None, "absolute_url", AbsoluteURL)
    ztapi.browserView(IContainmentRoot, "absolute_url", SiteAbsoluteURL)

    ztapi.browserView(None, '', AbsoluteURL, providing=IAbsoluteURL)
    ztapi.browserView(IContainmentRoot, '', SiteAbsoluteURL,
                      providing=IAbsoluteURL)


#------------------------------------------------------------------------
# Use registration
from zope.app.registration.interfaces import IAttributeRegisterable
from zope.app.registration.interfaces import IRegistered
from zope.app.registration.registration import Registered
def setUpRegistered():
    ztapi.provideAdapter(IAttributeRegisterable, IRegistered,
                         Registered)

#------------------------------------------------------------------------
# Service service lookup
from zope.app.component.localservice import serviceServiceAdapter
from zope.app.registration.interfaces import IRegistrationActivatedEvent
from zope.app.registration.interfaces import IRegistrationDeactivatedEvent
from zope.app.site.service import handleActivated, handleDeactivated
from zope.component.interfaces import IServiceService
from zope.interface import Interface
def setUpServiceService():
    ztapi.subscribe((IRegistrationActivatedEvent,), None, handleActivated)
    ztapi.subscribe((IRegistrationDeactivatedEvent,), None, handleDeactivated)
    ztapi.provideAdapter(Interface, IServiceService, serviceServiceAdapter)

#------------------------------------------------------------------------
# Placeful setup
import zope.app.component.hooks
from zope.app.testing.placelesssetup import setUp as placelessSetUp
from zope.app.testing.placelesssetup import tearDown as placelessTearDown
def placefulSetUp(site=False):
    placelessSetUp()
    zope.app.component.hooks.setHooks()
    setUpAnnotations()
    setUpDependable()
    setUpTraversal()
    setUpRegistered()
    setUpServiceService()

    if site:
        site = rootFolder()
        createServiceManager(site, setsite=True)
        return site

from zope.app.component.hooks import setSite
def placefulTearDown():
    placelessTearDown()
    zope.app.component.hooks.resetHooks()
    setSite()


from zope.app.folder import Folder, rootFolder

def buildSampleFolderTree():
    # set up a reasonably complex folder structure
    #
    #     ____________ rootFolder ____________
    #    /                                    \
    # folder1 __________________            folder2
    #   |                       \             |
    # folder1_1 ____           folder1_2    folder2_1
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

    return root


from zope.app.site.service import ServiceManager
from zope.app.site.interfaces import ISite
def createServiceManager(folder, setsite=False):
    if not ISite.providedBy(folder):
        folder.setSiteManager(ServiceManager(folder))
    if setsite:
        setSite(folder)
    return zapi.traverse(folder, "++etc++site")

from zope.app.site.service import ServiceRegistration
from zope.app.site.interfaces import ISimpleService
from zope.app.registration.interfaces import ActiveStatus

def addService(servicemanager, name, service, suffix=''):
    """Add a service to a service manager

    This utility is useful for tests that need to set up services.
    """
    # Most local services implement ISimpleService in ZCML; therefore make
    # sure we got it here as well.
    zope.interface.directlyProvides(service, ISimpleService)

    default = zapi.traverse(servicemanager, 'default')
    default[name+suffix] = service
    registration = ServiceRegistration(name, service, default)
    key = default.getRegistrationManager().addRegistration(registration)
    zapi.traverse(default.getRegistrationManager(), key).status = ActiveStatus
    return default[name+suffix]

from zope.app.utility import UtilityRegistration

def addUtility(servicemanager, name, iface, utility, suffix=''):
    """Add a utility to a service manager

    This utility is useful for tests that need to set up utilities.
    """
    
    folder_name = (name or (iface.__name__ + 'Utility')) + suffix
    default = zapi.traverse(servicemanager, 'default')
    default[folder_name] = utility
    registration = UtilityRegistration(name, iface, default[folder_name])
    key = default.getRegistrationManager().addRegistration(registration)
    zapi.traverse(default.getRegistrationManager(), key).status = ActiveStatus
    return default[folder_name]

def createStandardServices(folder):
    '''Create a bunch of standard placeful services

    Well, uh, 0
    '''
    sm = createServiceManager(folder)


