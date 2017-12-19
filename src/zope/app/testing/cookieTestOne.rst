========================
DocTest Functional Tests
========================

This file documents and tests doctest-based functional tests and basic
Zope web-application functionality.

This second DocTest, zope/app/testing/cookieTestOne.rst, has specifically
been created in order to make sure cookie information is not being saved
across a test suite. If we are saving these via a global 'http' instance,
we will see more results than those listed below. 'http' is instead
created in setUp within _prepare_doctest_keywords, rather than in the
global declarations.

Now we will run tests to ensure that cookies are not saved across doctests.

  >>> from zope.app.testing import functional
  >>> from zope.app.testing.tests import DummyCookiesResponse

We will create some cookie values and saved them in our 'http' value, which
is a CookieHandler() object.

  >>> response = DummyCookiesResponse(dict(
  ...     proton=dict(value='fromCookieTestOne',
  ...                 path='/foo',
  ...                 comment='rest is ignored'),
  ...     neutron=dict(value='fromCookieTestOne')))

If 'http' is created as a global variable, then every doctest in this
suite will be saving cookies in it, and one doctest may see cookies for
another doctest. We only want two cookies in 'http' - the ones we just
created.

  >>> http.saveCookies(response)
  >>> len(http.cookies)
  2

  >>> http.cookies['proton'].OutputString()
  'proton=fromCookieTestOne; Path=/foo...'

  >>> http.cookies
  <SimpleCookie: neutron='fromCookieTestOne' proton='fromCookieTestOne'>

  >>> http.cookies['proton'] = 'fromCookieTestOne'
  >>> http.cookies['proton']['path'] = '/foo'
  >>> http.cookies['electron'] = 'fromCookieTestOne'
  >>> http.cookies['electron']['path'] = '/foo/baz'
  >>> http.cookies['neutron'] = 'fromCookieTestOne'

  >>> cookieHeader = http.httpCookie('/foo/bar')
  >>> parts = cookieHeader.split('; ')
  >>> parts.sort()
  >>> parts
  ['neutron=fromCookieTestOne', 'proton=fromCookieTestOne']

  >>> cookieHeader = http.httpCookie('/foo/baz')
  >>> parts = cookieHeader.split('; ')
  >>> parts.sort()
  >>> parts
  ['electron=fromCookieTestOne',
   'neutron=fromCookieTestOne',
   'proton=fromCookieTestOne']
