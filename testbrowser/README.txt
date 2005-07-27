================
The Test Browser
================

The ``zope.app.testing.testbrowser`` module exposes a ``Browser`` class that
simulates a web browser similar to Mozilla Firefox or IE.

    >>> from zope.app.testing.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

The browser can `open` web pages:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')
    >>> browser.url
    'http://localhost/@@/testbrowser/simple.html'


Page Contents
-------------

The contents of the current page are available:

    >>> print browser.contents
    <html>
      <head>
        <title>Simple Page</title>
      </head>
      <body>
        <h1>Simple Page</h1>
      </body>
    </html>
    <BLANKLINE>

Making assertions about page contents are easy.

    >>> 'Simple Page' in browser.contents
    True

Utilizing the doctest facilities, it is better to do:

    >>> print browser.contents
    <html>
    ...
        <h1>Simple Page</h1>
    ...

Note: Unfortunately, ellipsis (...) cannot be used at the beginning of the
output.


Checking for HTML
-----------------

Not all URLs return HTML. Of course our simple page does:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')
    >>> browser.isHtml
    True

But if we load an image (or other binary file), we do not get HTML:

    >>> browser.open('http://localhost/@@/testbrowser/zope3logo.gif')
    >>> browser.isHtml
    False


HTML Page Title
----------------

Another useful helper property is the title:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')
    >>> browser.title
    'Simple Page'

If a page does not provide a title, it is simply ``None``:

    >>> browser.open('http://localhost/@@/testbrowser/notitle.html')
    >>> browser.title

However, if the output is not HTML, then an error will occur trying to access
the title:

    >>> browser.open('http://localhost/@@/testbrowser/zope3logo.gif')
    >>> browser.title
    Traceback (most recent call last):
    ...
    BrowserStateError: not viewing HTML


Headers
-------

As you can see, the `contents` of the browser does not return any HTTP
headers. The headers are accessible via a separate attribute:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')

The page's headers are also available as an httplib.HTTPMessage instance:

    >>> browser.headers
    <httplib.HTTPMessage instance...>

The headers can be accesed as a string:

    >>> print browser.headers
    Status: 200 Ok
    Content-Length: ...
    Content-Type: text/html;charset=utf-8
    X-Content-Type-Warning: guessed from content
    X-Powered-By: Zope (www.zope.org), Python (www.python.org)
    <BLANKLINE>

Or as a mapping:

    >>> browser.headers['content-type']
    'text/html;charset=utf-8'


Navigation
----------

    >>> browser.open('http://localhost/++etc++site/default')

If you want to simulate clicking on a link, there is a `click` method.

    >>> browser.click('RootErrorReportingUtility')
    >>> browser.url
    'http://localhost/++etc++site/default/RootErrorReportingUtility'

We'll navigate to a form and fill in some values and the submit the form.

    >>> browser.click('Configure')
    >>> browser.url
    'http://localhost/++etc++site/default/RootErrorReportingUtility/@@configure.html'


Forms
-----

The current page has a form on it, let's look at some of the controls:

    >>> browser.controls['keep_entries']
    '20'
    >>> browser.controls['copy_to_zlog']
    False

If we request a control that doesn't exist, an exception is raised.

    >>> browser.controls['does_not_exist']
    Traceback (most recent call last):
    ...
    KeyError: 'does_not_exist'

We want to change some of the form values and submit.

    >>> browser.controls['keep_entries'] = '40'
    >>> browser.controls['copy_to_zlog'] = True
    >>> browser.click('Save Changes')

Are our changes reflected on the resulting page?

    >>> browser.controls['keep_entries']
    '40'
    >>> browser.controls['copy_to_zlog']
    True

The `controls` object also has an `update()` method similar to that of
a dictionary:

    >>> browser.controls.update(dict(keep_entries='30', copy_to_zlog=False))
    >>> browser.click('Save Changes')
    >>> browser.controls['keep_entries']
    '30'
    >>> browser.controls['copy_to_zlog']
    False

Finding Specific Forms
----------------------

Because pages can have multiple forms with like-named controls, it is sometimes
neccesary to access forms by name or id.  The browser's `forms` attribute can
be used to do so.  The key value is the form's name or id.  If more than one 
form has the same name or id, the first one will be returned.

XXX these need to be re-targeted to pages registered just for this test
##    >>> # zope form and use that instead
##    >>> form = browser.forms['portlet_form']

The form exposes several attributes:

##    >>> form.name
##    'portlet_form'
##    >>> form.action
##    'http://localhost/++etc++site/default/...'
##    >>> form.method
##    'POST'
##    >>> form.id is None
##    True

The form's controls can also be accessed with the `controls` mapping.

##    >>> form.controls['portlet_action']
##    '...'

More Forms
----------

Now, let's navegate to a page with a slightly more complex form.

    >>> browser.click('Registration')
    >>> browser.click('Advanced Options')
    >>> browser.click('UtilityRegistration')

Is the expected control on the page?

    >>> 'field.permission' in browser.controls
    True

Good, let's retrieve it then:

    >>> permission = browser.getControl('field.permission')

What kind of control is it?
    
    >>> permission.type
    'select'

Is it a single- or multi-select?

    >>> permission.multiple
    False

What options are available for the "field.permission" control?

    >>> permission.options
    ['', 'zope.Public', ... 'zope.ManageContent', ... 'zope.View', ...]


We'll store the current setting so we can set it back later.

    >>> original_permission = permission.value

Let's set one of the options and submit the form.

    >>> permission.value = ['zope.Public']
    >>> browser.click('Change')

Ok, did our change take effect? (Note that the order may not be preserved for
multi-selects.)

    >>> browser.controls['field.permission'] == ['zope.Public']
    True

Let's set it back, so we don't mess anything up.

    >>> permission.value = original_permission
    >>> browser.click('Change')


Handling Errors
---------------

A very useful feature of the publisher is the automatic graceful handling of
application errors, such as invalid URLs:

    >>> browser.open('http://localhost/invalid')
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 404: Not Found

Note that the above error was thrown by ``urllib2`` and not by the
publisher. For debugging purposes, however, it can be very useful to see the
original exception caused by the application. In those cases you can set the
``handleErrors`` property of the browser to ``False``. It is defaulted to
``True``:

    >>> browser.handleErrors
    True

So when we tell the publisher not to handle the errors,    

    >>> browser.handleErrors = False

we get a different, Zope internal error:

    >>> browser.open('http://localhost/invalid')
    Traceback (most recent call last):
    ...
    NotFound: Object: <zope.app.folder.folder.Folder object at ...>, 
              name: u'invalid'
