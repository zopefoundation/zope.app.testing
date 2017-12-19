========================
DocTest Functional Tests
========================

This file documents and tests doctest-based functional tests and basic
Zope web-application functionality.

This second DocTest, zope/app/testing/cookieTestTwo.rst, has specifically
been created in order to make sure cookie information is not being saved
across a test suite. If we are saving these via a global 'http' instance,
we will see more results than those listed below. 'http' is instead
created in setUp within _prepare_doctest_keywords, rather than in the
global declarations.

  >>> from zope.app.testing import functional
  >>> from zope.app.testing.tests import DummyCookiesResponse

  >>> response = DummyCookiesResponse(dict(
  ...     cobalt=dict(value='fromCookieTestTwo',
  ...                 path='/foo',
  ...                 comment='rest is ignored'),
  ...     crimson=dict(value='fromCookieTestTwo')))

  >>> http.saveCookies(response)
  >>> len(http.cookies)
  2

  >>> http.cookies['cobalt'].OutputString()
  'cobalt=fromCookieTestTwo; Path=/foo...'

  >>> http.cookies
  <SimpleCookie: cobalt='fromCookieTestTwo' crimson='fromCookieTestTwo'>

  >>> http.cookies['cobalt'] = 'fromCookieTestTwo'
  >>> http.cookies['cobalt']['path'] = '/foo'
  >>> http.cookies['amber'] = 'fromCookieTestTwo'
  >>> http.cookies['amber']['path'] = '/foo/baz'
  >>> http.cookies['crimson'] = 'fromCookieTestTwo'

  >>> cookieHeader = http.httpCookie('/foo/bar')
  >>> parts = cookieHeader.split('; ')
  >>> parts.sort()
  >>> parts
  ['cobalt=fromCookieTestTwo', 'crimson=fromCookieTestTwo']

  >>> cookieHeader = http.httpCookie('/foo/baz')
  >>> parts = cookieHeader.split('; ')
  >>> parts.sort()
  >>> parts
  ['amber=fromCookieTestTwo',
   'cobalt=fromCookieTestTwo',
   'crimson=fromCookieTestTwo']
