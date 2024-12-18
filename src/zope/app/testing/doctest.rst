==========================
 DocTest Functional Tests
==========================

This file documents and tests doctest-based functional tests and basic
Zope web-application functionality.

Request/Response Functional Tests
=================================

You can create Functional tests as doctests.  Typically, this is done
by using a script such as src/zope/app/testing/dochttp.py to convert
tcpwatch recorded output to a doctest, which is then edited to provide
explanation and to remove uninteresting details.  That is how this
file was created.

Here we'll test some of the most basic types of access.

First, we'll test accessing a protected page without credentials:

  >>> print(http(r"""
  ... GET /@@contents.html HTTP/1.1
  ... """))
  HTTP/1.1 401 Unauthorized
  Cache-Control: no-store, no-cache, must-revalidate
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Expires: Mon, 26 Jul 1997 05:00:00 GMT
  Pragma: no-cache
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>
  <!DOCTYPE html PUBLIC ...

Here we see that we got:

  - A 401 response,
  - A WWW-Authenticate header, and
  - An html body with an error message
  - Some technical headers to keep squid happy

Note that we used ellipsis to indicate ininteresting details.

Next, we'll access the same page with credentials:

  >>> print(http(r"""
  ... GET /@@contents.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 OK
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <!DOCTYPE html PUBLIC ...

Important note: you must use the user named "mgr" with a password
"mgrpw".

And we get a normal output.

Next we'll try accessing site management. Since we used "/manage",
we got redirected:

  >>> print(http(r"""
  ... GET /++etc++site/@@manage HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Referer: http://localhost:8081/
  ... """))
  HTTP/1.1 303 See Other
  Content-Length: 0
  Content-Type: text/plain;charset=utf-8
  Location: @@contents.html
  <BLANKLINE>

Note that, in this case, we got a 303 response.  A 303 response is the
prefered response for this sort of redirect with HTTP 1.1.  If we used
HTTP 1.0, we'd get a 302 response:

  >>> print(http(r"""
  ... GET /++etc++site/@@manage HTTP/1.0
  ... Authorization: Basic mgr:mgrpw
  ... Referer: http://localhost:8081/
  ... """))
  HTTP/1.0 302 Moved Temporarily
  Content-Length: 0
  Content-Type: text/plain;charset=utf-8
  Location: @@contents.html
  <BLANKLINE>

Lets visit the page we were redirected to:

  >>> print(http(r"""
  ... GET /++etc++site/@@contents.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Referer: http://localhost:8081/
  ... """))
  HTTP/1.1 200 OK
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <!DOCTYPE html PUBLIC ...

Finally, lets access the default page for the site:

  >>> print(http(r"""
  ... GET / HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 OK
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  <BLANKLINE>
  <!DOCTYPE html PUBLIC ...

Access to the object system
===========================

You can use the `getRootFolder()` function:

  >>> root = getRootFolder()
  >>> root
  <zope.site.folder.Folder object at ...>

You can intermix HTTP requests with regular Python calls.  Note,
however, that making an `http()` call implied a transaction commit.
If you want to throw away changes made in Python code, abort the
transaction before the HTTP request.

  >>> print(http(r"""
  ... POST /@@contents.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Length: 58
  ... Content-Type: application/x-www-form-urlencoded
  ...
  ... type_name=BrowserAdd__zope.site.folder.Folder&new_value=f1""",
  ... handle_errors=False))
  HTTP/1.1 303 See Other
  Content-Length: ...
  Content-Type: text/html;charset=utf-8
  Location: http://localhost/@@contents.html
  <BLANKLINE>
  <!DOCTYPE html ...

Now we can see that the new folder was added:

  >>> [str(x) for x in root.keys()]
  ['f1']
