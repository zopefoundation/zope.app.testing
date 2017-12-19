Zope Publisher Browser Tests
============================

These tests specifically test the implementation of Browser which uses the Zope
Publisher via zope.app.testing as the application to test.

    >>> from zope.app.testing.testbrowser import Browser
    >>> browser = Browser()

Error Handling
--------------

handleErrors works as advertised:
    
    >>> browser.handleErrors
    True
    >>> browser.open('http://localhost/invalid')
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 404: Not Found

So when we tell the publisher not to handle the errors,

    >>> browser.handleErrors = False
    >>> browser.open('http://localhost/invalid')
    Traceback (most recent call last):
    ...
    NotFound: Object: <zope.site.folder.Folder object at ...>,
              name: u'invalid'

Spaces in URLs
--------------

Spaces in URLs don't cause blowups:

    >>> browser.open('http://localhost/space here')
    Traceback (most recent call last):
    ...
    NotFound: Object: <zope.site.folder.Folder object at ...>,
              name: u'space here'

Headers
-------

Sending arbitrary headers works:

    >>> browser.addHeader('Accept-Language', 'en-US')
    >>> browser.open('http://localhost/echo_one?var=HTTP_ACCEPT_LANGUAGE')
    >>> print browser.contents
    'en-US'

POST
----

HTTP posts are correctly sent:

    >>> browser.post('http://localhost/echo', 'x=1&y=2')
    >>> print browser.contents
    CONTENT_LENGTH: 7
    CONTENT_TYPE: application/x-www-form-urlencoded
    HTTP_ACCEPT_LANGUAGE: en-US
    HTTP_CONNECTION: close
    HTTP_COOKIE:
    HTTP_HOST: localhost
    HTTP_USER_AGENT: Python-urllib/2.4
    PATH_INFO: /echo
    QUERY_STRING:
    REMOTE_ADDR: 127.0.0.1
    REQUEST_METHOD: POST
    SERVER_PROTOCOL: HTTP/1.1
    x: 1
    y: 2
    Body: ''
    
Returned headers
----------------

Server headers are correctly returned:

    >>> print browser.headers
    Status: 200 OK
    Content-Length: 123
    Content-Type: text/plain;charset=utf-8
    X-Content-Type-Warning: guessed from content
    X-Powered-By: Zope (www.zope.org), Python (www.python.org)
