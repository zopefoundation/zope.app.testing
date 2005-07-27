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
headers. The headers are accessible via a separate attribute, which is an
``httplib.HTTPMessage`` instance:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')
    >>> browser.headers
    <httplib.HTTPMessage instance...>

The headers can be accesed as a string:

    >>> print browser.headers
    Status: 200 Ok
    Content-Length: ...
    Content-Type: text/html;charset=utf-8
    X-Content-Type-Warning: guessed from content
    X-Powered-By: Zope (www.zope.org), Python (www.python.org)

Or as a mapping:

    >>> browser.headers['content-type']
    'text/html;charset=utf-8'


Navigation
----------

If you want to simulate clicking on a link, there is a `click` method. In the
`navigate.html` file there are several links setup to demonstrate the
capabilities of the `click` method. 

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')

The simplest is to access the link by the text value that is linked, in other
words the linked text you would see in a browser:

    >>> print browser.contents
    <html>
    ...
    <a href="navigate.html?message=By+Link+Text">Link Text</a>
    ...

    >>> browser.click('Link Text')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html?message=By+Link+Text'
    >>> print browser.contents
    <html>
    ...
    Message: <em>By Link Text</em>
    ...

You can also find the link by (1) its URL,

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')
    >>> print browser.contents
    <html>
    ...
    <a href="navigate.html?message=By+URL">Using the URL</a>
    ...

    >>> browser.click(url='\?message=By\+URL')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html?message=By+URL'
    >>> print browser.contents
    <html>
    ...
    Message: <em>By URL</em>
    ...

and (2) its id:

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')
    >>> print browser.contents
    <html>
    ...
    <a href="navigate.html?message=By+Id" id="anchorid">By Anchor Id</a>
    ...

    >>> browser.click(id='anchorid')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html?message=By+Id'
    >>> print browser.contents
    <html>
    ...
    Message: <em>By Id</em>
    ...

But there are more interesting cases. You can also use the `click` method to
submit forms. You can either use the submit button's value by simply
specifying the text:

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')
    >>> print browser.contents
    <html>
    ...
    <input type="submit" name="submit-form" value="Submit" />
    ...

    >>> browser.click('Submit')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html'
    >>> print browser.contents
    <html>
    ...
    Message: <em>By Form Submit</em>
    ...

Alternatively, you can specify the name of the control:

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')
    >>> browser.click(name='submit-form')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html'
    >>> print browser.contents
    <html>
    ...
    Message: <em>By Form Submit</em>
    ...

You thought we were done here? Not so quickly. The `click` method also
supports image maps, though not by specifying the coordinates, but using the
area's title (or other tag attgributes):

    >>> browser.open('http://localhost/@@/testbrowser/navigate.html')
    >>> browser.click(id='zope3')
    >>> browser.url
    'http://localhost/@@/testbrowser/navigate.html?message=Zope+3+Name'
    >>> print browser.contents
    <html>
    ...
    Message: <em>Zope 3 Name</em>
    ...


Other Navigation
----------------

Like in any normal browser, you can reload a page:

    >>> browser.open('http://localhost/@@/testbrowser/simple.html')
    >>> browser.url
    'http://localhost/@@/testbrowser/simple.html'
    >>> browser.reload()
    >>> browser.url
    'http://localhost/@@/testbrowser/simple.html'

You can also go back:

    >>> browser.open('http://localhost/@@/testbrowser/notitle.html')
    >>> browser.url
    'http://localhost/@@/testbrowser/notitle.html'
    >>> browser.goBack()
    >>> browser.url
    'http://localhost/@@/testbrowser/simple.html'


Controls
--------

One of the most important features of the browser is the ability to inspect
and fill in values for the controls of input forms.


Forms
-----

   >>> browser.open('http://localhost/++etc++site/default/RootErrorReportingUtility/@@configure.html')


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
