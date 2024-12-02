##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Test tcpdoc

"""
import io
import os
import re
import unittest
from doctest import DocTestSuite

import transaction
from ZODB.interfaces import IDatabase
from zope.app.publication.requestpublicationfactories import BrowserFactory
from zope.app.publication.requestpublicationregistry import factoryRegistry
from zope.testing.renormalizing import RENormalizing

import zope.app.testing
from zope.app.testing import functional
from zope.app.testing.dochttp import dochttp
from zope.app.testing.functional import BrowserTestCase
from zope.app.testing.functional import FunctionalDocFileSuite
from zope.app.testing.functional import FunctionalTestCase
from zope.app.testing.functional import HTTPTestCase
from zope.app.testing.functional import SampleFunctionalTest
from zope.app.testing.testing import AppTestingLayer
from zope.app.testing.testing import FailingKlass


HEADERS = """\
HTTP/1.1 200 OK
Content-Type: text/plain
"""

BODY = """\
This is the response body.
"""

here = os.path.dirname(zope.app.testing.__file__)
directory = os.path.join(here, 'recorded')

expected = r'''

  >>> print(http(r"""
  ... GET /@@contents.html HTTP/1.1
  ... """))
  HTTP/1.1 401 Unauthorized
  Content-Length: 89
  Content-Type: text/html;charset=utf-8
  Www-Authenticate: basic realm="Zope"
  <BLANKLINE>
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en">
  <BLANKLINE>
  ...
  <BLANKLINE>
  </html>
  <BLANKLINE>
  <BLANKLINE>


  >>> print(http(r"""
  ... GET /@@contents.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... """))
  HTTP/1.1 200 OK
  Content-Length: 89
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en">
  <BLANKLINE>
  ...
  <BLANKLINE>
  </html>
  <BLANKLINE>
  <BLANKLINE>


  >>> print(http(r"""
  ... GET /++etc++site/@@manage HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/
  ... """))
  HTTP/1.1 303 See Other
  Content-Length: 0
  Content-Type: text/plain;charset=utf-8
  Location: @@tasks.html
  <BLANKLINE>


  >>> print(http(r"""
  ... GET / HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... """))
  HTTP/1.1 200 OK
  Content-Length: 89
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en">
  <BLANKLINE>
  ...
  <BLANKLINE>
  </html>
  <BLANKLINE>
  <BLANKLINE>


  >>> print(http(r"""
  ... GET /++etc++site/@@tasks.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/
  ... """))
  HTTP/1.1 200 OK
  Content-Length: 89
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en">
  <BLANKLINE>
  ...
  <BLANKLINE>
  </html>
  <BLANKLINE>
  <BLANKLINE>
'''


class FunctionalHTTPDocTest(unittest.TestCase):
    maxDiff = None

    def test_dochttp(self):
        capture = io.StringIO()
        dochttp(['-p', 'test', directory], output_fp=capture)
        got = capture.getvalue()
        self.assertEqual(expected, got)

    def test_no_argument(self):
        import sys
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            with self.assertRaises(SystemExit) as exc:
                dochttp(["-p", 'test'])
        finally:
            sys.stderr = old_stderr

        e = exc.exception
        self.assertEqual(e.args, (2,))

    def test_bad_directory_argument(self):
        import shutil
        import tempfile
        d = tempfile.mkdtemp('.zope.app.testing')
        self.addCleanup(shutil.rmtree, d)

        with open(os.path.join(d, 'test1.request'), 'w') as f:
            f.write("Fake request file")
        with open(os.path.join(d, 'test1.response'), 'w') as f:
            f.write("")

        with self.assertRaisesRegex(
                SystemExit,
                "Expected equal numbers of requests and responses in '" + d):
            dochttp(["-p", 'test', d])


class AuthHeaderTestCase(unittest.TestCase):

    def test_auth_encoded(self):
        auth_header = functional.auth_header
        header = 'Basic Z2xvYmFsbWdyOmdsb2JhbG1ncnB3'
        self.assertEqual(auth_header(header), header)

    def test_auth_non_encoded(self):
        auth_header = functional.auth_header
        header = 'Basic globalmgr:globalmgrpw'
        expected = 'Basic Z2xvYmFsbWdyOmdsb2JhbG1ncnB3'
        self.assertEqual(auth_header(header), expected)

    def test_auth_non_encoded_empty(self):
        auth_header = functional.auth_header
        header = 'Basic globalmgr:'
        expected = 'Basic Z2xvYmFsbWdyOg=='
        self.assertEqual(auth_header(header), expected)
        header = 'Basic :pass'
        expected = 'Basic OnBhc3M='
        self.assertEqual(auth_header(header), expected)

    def test_auth_non_encoded_colon(self):
        auth_header = zope.app.testing.functional.auth_header
        header = 'Basic globalmgr:pass:pass'
        expected = 'Basic Z2xvYmFsbWdyOnBhc3M6cGFzcw=='
        self.assertEqual(auth_header(header), expected)


class HTTPCallerTestCase(unittest.TestCase):

    def test_chooseRequestClass(self):
        from zope.publisher.interfaces import IPublication
        from zope.publisher.interfaces import IRequest

        factoryRegistry.register('GET', '*', 'browser', 0, BrowserFactory())

        caller = functional.HTTPCaller()
        request_class, publication_class = caller.chooseRequestClass(
            method='GET', path='/', environment={})

        self.assertTrue(IRequest.implementedBy(request_class))
        self.assertTrue(IPublication.implementedBy(publication_class))


class DummyCookiesResponse:
    # Ugh, this simulates the *internals* of a HTTPResponse object
    # TODO: expand the IHTTPResponse interface to give access to all cookies
    _cookies = None

    def __init__(self, cookies=None):
        self._cookies = cookies or {}


class CookieHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = functional.CookieHandler()

    def test_saveCookies(self):
        response = DummyCookiesResponse(dict(
            spam=dict(value='eggs', path='/foo', comment='rest is ignored'),
            monty=dict(value='python')))
        self.handler.saveCookies(response)
        self.assertEqual(len(self.handler.cookies), 2)
        self.assertIn(self.handler.cookies['spam'].OutputString(),
                      ('spam=eggs; Path=/foo;', 'spam=eggs; Path=/foo'))
        self.assertIn(self.handler.cookies['monty'].OutputString(),
                      ('monty=python;', 'monty=python'))

    def test_httpCookie(self):
        cookies = self.handler.cookies
        cookies['spam'] = 'eggs'
        cookies['spam']['path'] = '/foo'
        cookies['bar'] = 'baz'
        cookies['bar']['path'] = '/foo/baz'
        cookies['monty'] = 'python'

        cookieHeader = self.handler.httpCookie('/foo/bar')
        parts = sorted(cookieHeader.split('; '))
        self.assertEqual(parts, ['monty=python', 'spam=eggs'])

        cookieHeader = self.handler.httpCookie('/foo/baz')
        parts = cookieHeader.split('; ')
        parts.sort()
        self.assertEqual(parts, ['bar=baz', 'monty=python', 'spam=eggs'])

    # There is no test for CookieHandler.loadCookies because it that method
    # only passes the arguments on to Cookie.BaseCookie.load, which the
    # standard library has tests for (we hope).


class HTTPFunctionalTest(HTTPTestCase):

    def testNoDefaultReferer(self):
        # There should be no referer set in the request by default.
        r = self.makeRequest()
        self.assertRaises(KeyError, r.environment.__getitem__, 'HTTP_REFERER')


class BrowserFunctionalTest(BrowserTestCase):

    def testNoDefaultReferer(self):
        # There should be no referer set in the request by default.
        r = self.makeRequest()
        self.assertRaises(KeyError, r.environment.__getitem__, 'HTTP_REFERER')


class HTTPCallerFunctionalTest(FunctionalTestCase):

    def testNoDefaultReferer(self):
        # There should be no referer set in the request by default.
        from zope.app.testing.functional import HTTPCaller
        http = HTTPCaller()
        response = http("GET /++skin++Basic HTTP/1.1\n\n")
        self.assertRaises(KeyError, response._request.environment.__getitem__,
                          'HTTP_REFERER')

    def testRemoteAddr(self):
        # There should be a REMOTE_ADDR in the request by default.
        from zope.app.testing.functional import HTTPCaller
        http = HTTPCaller()
        response = http("GET / HTTP/1.1\n\n")
        self.assertEqual(response._request.environment['REMOTE_ADDR'],
                         '127.0.0.1')


class GetCookies:
    """Get all cookies set."""

    def __call__(self):
        cookies = sorted([f'{k}={v}'
                          for k, v in self.request.getCookies().items()])
        return ';'.join(cookies)


class SetCookies:
    """Set a specific cookie."""

    def __call__(self):
        self.request.response.setCookie('bid', 'bval')


class CookieFunctionalTest(BrowserTestCase):

    """Functional tests should handle cookies like a web browser

    Multiple requests in the same test should acumulate cookies.
    We also ensure that cookies with path values are only sent for
    the correct URL's so we can test cookies don't 'leak'. Expiry,
    secure and other cookie attributes are not being worried about
    at the moment

    """

    def setUp(self):
        import zope.configuration.xmlconfig

        super().setUp()
        self.assertEqual(
            len(self.cookies.keys()), 0,
            'cookies store should be empty')

        zope.configuration.xmlconfig.string(r'''
        <configure xmlns="http://namespaces.zope.org/browser">

           <include package="zope.browserpage" file="meta.zcml" />

           <page
              name="getcookies"
              for="*"
              permission="zope.Public"
              class="zope.app.testing.tests.GetCookies" />

           <page
              name="setcookie"
              for="*"
              permission="zope.Public"
              class="zope.app.testing.tests.SetCookies" />

        </configure>
        ''')

    def testDefaultCookies(self):
        # By default no cookies are set
        response = self.publish('/')
        self.assertEqual(response.getStatus(), 200)
        self.assertFalse(response._request._cookies)

    def testSimpleCookies(self):
        self.cookies['aid'] = 'aval'
        response = self.publish('/')
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response._request._cookies['aid'], 'aval')

    def testCookiePaths(self):
        # We only send cookies if the path is correct
        self.cookies['aid'] = 'aval'
        self.cookies['aid']['Path'] = '/sub/folder'
        self.cookies['bid'] = 'bval'
        response = self.publish('/')

        self.assertEqual(response.getStatus(), 200)
        self.assertNotIn('aid', response._request._cookies)
        self.assertEqual(response._request._cookies['bid'], 'bval')

    def testHttpCookieHeader(self):
        # Passing an HTTP_COOKIE header to publish adds cookies
        response = self.publish('/', env={
            'HTTP_COOKIE':
                '$Version=1, aid=aval; $Path=/sub/folder, bid=bval'})
        self.assertEqual(response.getStatus(), 200)
        self.assertNotIn('aid', response._request._cookies)
        self.assertEqual(response._request._cookies['bid'], 'bval')

    def testStickyCookies(self):
        # Cookies should acumulate during the test
        response = self.publish('/', env={'HTTP_COOKIE': 'aid=aval;'})
        self.assertEqual(response.getStatus(), 200)

        # Cookies are implicity passed to further requests in this test
        response = self.publish('/getcookies')
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getBody().strip(), 'aid=aval')

        # And cookies set in responses also acumulate
        response = self.publish('/setcookie')
        self.assertEqual(response.getStatus(), 200)
        response = self.publish('/getcookies')
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getBody().strip(), 'aid=aval;bid=bval')


class SkinsAndHTTPCaller(FunctionalTestCase):

    def test_skins(self):
        # Regression test for http://zope.org/Collectors/Zope3-dev/353
        from zope.app.testing.functional import HTTPCaller
        http = HTTPCaller()
        response = http("GET /++skin++Basic HTTP/1.1\n\n")
        self.assertIn("zopetopBasic.css", str(response))


class RetryProblemFunctional(FunctionalTestCase):

    def setUp(self):
        super().setUp()

        root = self.getRootFolder()

        root['fail'] = FailingKlass()

        transaction.commit()

    def tearDown(self):
        root = self.getRootFolder()
        del root['fail']
        super().tearDown()

    def test_retryOnConflictErrorFunctional(self):
        from zope.app.testing.functional import HTTPCaller

        http = HTTPCaller()
        response = http(r"""
GET /@@test-conflict-raise-view.html HTTP/1.1
Authorization: Basic mgr:mgrpw
""")

        self.assertNotEqual(response.getStatus(), 599)
        self.assertEqual(response.getStatus(), 500)


class RetryProblemBrowser(BrowserTestCase):
    def setUp(self):
        super().setUp()

        root = self.getRootFolder()

        root['fail'] = FailingKlass()

        transaction.commit()

    def tearDown(self):
        root = self.getRootFolder()
        del root['fail']
        super().tearDown()

    def test_retryOnConflictErrorBrowser(self):
        response = self.publish('/@@test-conflict-raise-view.html',
                                handle_errors=True)
        self.assertNotEqual(response.getStatus(), 599)
        self.assertEqual(response.getStatus(), 500)


ftesting_zcml = os.path.join(here, 'ftesting.zcml')


def doctest_FunctionalTestSetup_clears_global_utilities():
    """Test that FunctionalTestSetup doesn't leave global utilities.

    Leaving global IDatabase utilities makes a nice juicy memory leak.
    See https://bugs.launchpad.net/zope3/+bug/251273

    This bug has now been fixed and this test exercises the fixed version.

        >>> from zope.app.testing.functional import FunctionalTestSetup
        >>> setup = FunctionalTestSetup(ftesting_zcml)

    At this point, there are registrations for the base databases created by
    the initialization:

        >>> from zope.component import getAllUtilitiesRegisteredFor
        >>> base, = getAllUtilitiesRegisteredFor(IDatabase)

    Setting up for a test causes overriding registrations to be made:

        >>> setup.setUp()
        >>> dbs = list(getAllUtilitiesRegisteredFor(IDatabase))
        >>> len(dbs)
        1
        >>> base in dbs
        False
        >>> override, = dbs

    Tearing down the test context causes the overriding database to be
    removed:

        >>> setup.tearDown()
        >>> list(getAllUtilitiesRegisteredFor(IDatabase))
        []

    Tearing down completely:

        >>> setup.tearDownCompletely()
    """


empty_zcml = os.path.join(here, 'empty.zcml')


def doctest_FunctionalTestSetup_supports_product_config():
    """Test that FunctionalTestSetup configures products.

    We want to apply the following product configuration before opening
    databases:

        >>> product_config = '''
        ... <product-config abc>
        ...  key1 value1
        ...  key2 value2
        ... </product-config>
        ... '''

    Since we expect the product configuration to be available when the layer
    is initialized, we'll register a subscriber for the IDatabaseOpenedEvent
    event, The normal CA-provided handling of the event is of no use to use,
    since the functional layer controls the configuration of that, but a
    low-level zoe.event subscriber will do the job:

        >>> import zope.event

        >>> def handle_database_open(event):
        ...     global config
        ...     IDbOE = zope.processlifetime.IDatabaseOpened
        ...     if IDbOE.providedBy(event):
        ...         config = zope.app.appsetup.product.getProductConfiguration(
        ...             'abc')

        >>> zope.event.subscribers.append(handle_database_open)

    The product configuration is passed to the layer setup and installed by
    the setUp method:

        >>> import pprint
        >>> import zope.app.appsetup.product
        >>> from zope.app.testing.functional import FunctionalTestSetup

        >>> setup = FunctionalTestSetup(
        ...     empty_zcml, product_config=product_config)

    The configuration was visible to our database-opened subscriber:

        >>> pprint.pprint(config, width=1)
        {'key1': 'value1',
         'key2': 'value2'}

        >>> config = zope.app.appsetup.product.getProductConfiguration(
        ...     'abc')
        >>> pprint.pprint(config, width=1)
        {'key1': 'value1',
         'key2': 'value2'}

    Let's run a test that mutates the product configuration:

        >>> setup.setUp()
        >>> zope.app.appsetup.product.setProductConfiguration(
        ...     'abc', {'another': 'value'})
        >>> zope.app.appsetup.product.getProductConfiguration('abc')
        {'another': 'value'}
        >>> setup.tearDown()

    A second test run in the layer sees the original product configuration:

        >>> setup.setUp()
        >>> config = zope.app.appsetup.product.getProductConfiguration(
        ...     'abc')
        >>> pprint.pprint(config, width=1)
        {'key1': 'value1',
         'key2': 'value2'}
        >>> setup.tearDown()

    After the layer is cleaned up, there's no longer any product
    configuration:

        >>> zope.event.subscribers.remove(handle_database_open)
        >>> setup.tearDownCompletely()

        >>> zope.app.appsetup.product.saveConfiguration()
        {}

    """


def doctest_ZCMLLayer_carries_product_configuration():
    """Show that ``ZCMLLayer`` carries along product configuration.

    ZCML layers can carry be defined to work with specific product
    configuration; this is useful when application code (early subscribers,
    including generations) need configuration data.

    Let's define a couple of separate ZCML layers, and show that the
    configuration data is properly associated with each, and applied at
    appropriate times.

    We'll need two distinct product configurations:

        >>> product_config_one = '''
        ... <product-config abc>
        ...  key1 a1
        ...  key2 a2
        ... </product-config>
        ... '''

        >>> product_config_two = '''
        ... <product-config abc>
        ...  key1 b1
        ...  key2 b2
        ... </product-config>
        ... '''

    We can create two distinct layers that use these configurations:

        >>> LayerOne = functional.ZCMLLayer(
        ...     empty_zcml, 'zope.app.testing.tests', 'LayerOne',
        ...     product_config=product_config_one,
        ...     allow_teardown=True)

        >>> LayerTwo = functional.ZCMLLayer(
        ...     empty_zcml, 'zope.app.testing.tests', 'LayerTwo',
        ...     product_config=product_config_two,
        ...     allow_teardown=True)

    For each layer, we can see that the correct product configuration is
    installed, and subsequent layer usages won't have problems because of the
    previously installed layer.  This checks that initialization and
    deconstruction of the functional test setup is handled properly to allow
    layers to be used in sequence.

    Let's use a helper function to show the configuration:

        >>> import pprint

        >>> def show_config():
        ...     c = zope.app.appsetup.product.getProductConfiguration('abc')
        ...     pprint.pprint(c, width=1)

        >>> LayerOne.setUp()
        >>> show_config()
        {'key1': 'a1',
         'key2': 'a2'}

        >>> LayerOne.tearDown()

        >>> LayerTwo.setUp()
        >>> show_config()
        {'key1': 'b1',
         'key2': 'b2'}

        >>> LayerTwo.tearDown()

    """


class TestXMLRPCTransport(unittest.TestCase):

    def _makeOne(self):
        from zope.app.testing.xmlrpc import ZopeTestTransport
        return ZopeTestTransport()

    def test_construct(self):
        self._makeOne()


class TestXMLRPCServerProxy(unittest.TestCase):

    def _makeOne(self, uri, **kwargs):
        from zope.app.testing.xmlrpc import ServerProxy
        return ServerProxy(uri, **kwargs)

    def test_construct(self):
        self._makeOne("http://example.com")


class TestConflictRaisingView(unittest.TestCase):

    def _makeOne(self, context=None, request=None):
        from zope.app.testing.testing import ConflictRaisingView
        return ConflictRaisingView(context, request)

    def test_browserDefault(self):
        view = self._makeOne()
        self.assertEqual(view.browserDefault(), (view, ()))

    def test_call(self):
        from ZODB.POSException import ConflictError
        view = self._makeOne()
        with self.assertRaises(ConflictError):
            view()


class TestPlacefulSetUp(unittest.TestCase):

    def setUp(self):
        from zope.app.testing.setup import placefulSetUp
        self.site = placefulSetUp(True)

    def tearDown(self):
        from zope.app.testing.setup import placefulTearDown
        placefulTearDown()
        self.site = None

    def testSite(self):
        from zope.component.hooks import getSite
        self.assertEqual(self.site, getSite())

    def test_buildSampleFolderTree(self):
        from zope.app.testing.setup import buildSampleFolderTree

        t = buildSampleFolderTree()
        self.assertTrue(t)


def test_suite():
    import doctest

    from zope.app.testing.setup import setUpTestAsModule
    from zope.app.testing.setup import tearDownTestAsModule

    checker = RENormalizing([
        (re.compile(r'^HTTP/1.1 (\d{3}) .*?\n'), 'HTTP/1.1 \\1\n')])
    SampleFunctionalTest.layer = AppTestingLayer
    CookieFunctionalTest.layer = AppTestingLayer
    SkinsAndHTTPCaller.layer = AppTestingLayer
    RetryProblemFunctional.layer = AppTestingLayer
    RetryProblemBrowser.layer = AppTestingLayer
    HTTPFunctionalTest.layer = AppTestingLayer
    BrowserFunctionalTest.layer = AppTestingLayer
    HTTPCallerFunctionalTest.layer = AppTestingLayer

    doc_test = FunctionalDocFileSuite(
        'doctest.rst', 'cookieTestOne.rst',
        'cookieTestTwo.rst', checker=checker)
    doc_test.layer = AppTestingLayer

    xml_checker = RENormalizing((
        (re.compile('<DateTime \''), '<DateTime u\''),
        (re.compile('at [-0-9a-fA-F]+'), 'at <SOME ADDRESS>'),
        (re.compile("HTTP/1.0"), "HTTP/1.1"),
    ))

    def xmlSetUp(test):
        setUpTestAsModule(test, 'zope.app.testing.xmlrpc.README')

    def xmlTearDown(test):
        # clean up the views we registered:

        # we use the fact that registering None unregisters whatever is
        # registered. We can't use an unregistration call because that
        # requires the object that was registered and we don't have that handy.
        # (OK, we could get it if we want. Maybe later.)
        from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
        from zope.site.interfaces import IFolder

        zope.component.provideAdapter(None, (
            IFolder,
            IXMLRPCRequest
        ), zope.interface, 'contents')

        tearDownTestAsModule(test)

    xmlrpcsuite = FunctionalDocFileSuite(
        'xmlrpc.rst',
        setUp=xmlSetUp,
        tearDown=xmlTearDown,
        checker=xml_checker,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
    xmlrpcsuite.layer = AppTestingLayer

    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        DocTestSuite(),
        doc_test,
        xmlrpcsuite,
    ))
