===============
 XML-RPC views
===============

.. This file is copied (with slight modifications) from
   zope.app.publisher.xmlrpc:README.rst

XML-RPC Methods
===============

There are two ways to write XML-RPC views. You can write views that
provide "methods" for other objects, and you can write views that have
their own methods.  Let's look at the former case first, since it's a
little bit simpler.

Let's write a view that returns a folder listing:

  >>> class FolderListing(object):
  ...     def contents(self):
  ...         return sorted(self.context.keys())

Now we'll register it as a view:

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...   <include package="zope.security" />
  ...   <xmlrpc:view
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="contents"
  ...       class="zope.app.testing.xmlrpc.README.FolderListing"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Now, we'll add some items to the root folder:

  >>> print(http(r"""
  ... POST /@@contents.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Length: 58
  ... Content-Type: application/x-www-form-urlencoded
  ...
  ... type_name=BrowserAdd__zope.site.folder.Folder&new_value=f1"""))
  HTTP/1.1 303 See Other
  ...

  >>> print(http(r"""
  ... POST /@@contents.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Length: 58
  ... Content-Type: application/x-www-form-urlencoded
  ...
  ... type_name=BrowserAdd__zope.site.folder.Folder&new_value=f2"""))
  HTTP/1.1 303 See Other
  ...

And call our xmlrpc method:

  >>> from zope.app.testing.xmlrpc import ServerProxy
  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.contents()
  ['f1', 'f2']

Note that we get an unauthorized error if we don't supply authentication
credentials:

  >>> proxy = ServerProxy("http://localhost/", handleErrors=False)
  >>> proxy.contents()
  Traceback (most recent call last):
  ...
  zope.security.interfaces.Unauthorized: ...


Named XML-RPC Views
===================

Now let's look at views that have their own methods or other
subobjects.  Views that have their own methods have names that appear
in URLs and they get traversed to get to their methods, as in::

   .../somefolder/listing/contents

To make this possible, the view has to support traversal, so that,
when it is traversed, it traverses to its attributes.  To support
traversal, you can implement or provide an adapter to
`zope.publisher.interfaces.IPublishTraverse`. It's actually better to
provide an adapter so that accesses to attributes during traversal are
mediated by the security machinery.  (Object methods are always bound
to unproxied objects, but adapters are bound to proxied objects unless
they are trusted adapters.)

The 'zope.app.publisher.xmlrpc' package provides a base class,
`MethodPublisher`,  that provides the necessary traversal support.  In
particular, it has an adapter that simply traverses to attributes.

If an XML-RPC view isn't going to be public, then it also has to
implement 'zope.location.ILocation' so that security grants can be
acquired for it, at least with Zope's default security policy. The
`MethodPublisher` class does that too.

Let's modify our view class to use `MethodPublisher`:

  >>> from zope.app.publisher.xmlrpc import MethodPublisher

  >>> class FolderListing(MethodPublisher):
  ...
  ...     def contents(self):
  ...         return sorted(self.context.keys())

Note that `MethodPublisher` also provides a suitable `__init__`
method, so we don't need one any more.  This time, we'll register it
as as a named view:

  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...
  ...   <xmlrpc:view
  ...       name="listing"
  ...       for="zope.site.folder.IFolder"
  ...       methods="contents"
  ...       class="zope.app.testing.xmlrpc.README.FolderListing"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Now, when we access the `contents`, we do so through the listing view:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/listing/")
  >>> proxy.contents()
  ['f1', 'f2']
  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.listing.contents()
  ['f1', 'f2']

as before, we will get an error if we don't supply credentials:

  >>> proxy = ServerProxy("http://localhost/listing/", handleErrors=False)
  >>> proxy.contents()
  Traceback (most recent call last):
  ...
  zope.security.interfaces.Unauthorized: ...

Parameters
==========

Of course, XML-RPC views can take parameters, too:

  >>> class ParameterDemo:
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def add(self, first, second):
  ...         return first + second

Now we'll register it as a view:

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...
  ...   <xmlrpc:view
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="add"
  ...       class="zope.app.testing.xmlrpc.README.ParameterDemo"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Then we can issue a remote procedure call with a parameter and get
back, surprise!, the sum:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.add(20, 22)
  42

Faults
======

If you need to raise an error, the prefered way to do it is via an
`xmlrpclib.Fault`:

  >>> import xmlrpc.client as xmlrpclib

  >>> class FaultDemo:
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def your_fault(self):
  ...         return xmlrpclib.Fault(42, "It's your fault!")

Now we'll register it as a view:

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...
  ...   <xmlrpc:view
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="your_fault"
  ...       class="zope.app.testing.xmlrpc.README.FaultDemo"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Now, when we call it, we get a proper XML-RPC fault:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.your_fault()
  Traceback (most recent call last):
  xmlrpc.client.Fault: <Fault 42: "It's your fault!">


DateTime values
===============

`xmlrpclib` supports the native
`datetime.datetime` class.  Previously, DateTime
values needed to be encoded as `xmlrpclib.DateTime` instances:


  >>> class DateTimeDemo:
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def epoch_xml(self):
  ...         return xmlrpclib.DateTime("19700101T01:00:01")
  ...
  ...     def epoch_native(self):
  ...         import datetime
  ...         return datetime.datetime(1970, 1, 1, 1, 0, 1)

Now we'll register it as a view:

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...
  ...   <xmlrpc:view
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="epoch_xml epoch_native"
  ...       class="zope.app.testing.xmlrpc.README.DateTimeDemo"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Now, when we call either method, we get a DateTime value

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.epoch_xml()
  <DateTime u'19700101T01:00:01' at ...>
  >>> proxy.epoch_native()
  <DateTime u'1970-01-01T01:00:01' at ...>


Protecting XML/RPC views with class-based permissions
=====================================================

When setting up an XML/RPC view with no permission, the permission check is
deferred to the class that provides the view's implementation:

  >>> class ProtectedView(object):
  ...     def public(self):
  ...         return u'foo'
  ...     def protected(self):
  ...         return u'bar'

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...   <include package="zope.security" file="meta.zcml" />
  ...
  ...   <class class="zope.app.testing.xmlrpc.README.ProtectedView">
  ...       <require permission="zope.ManageContent"
  ...           attributes="protected" />
  ...       <allow attributes="public" />
  ...   </class>
  ...
  ...   <xmlrpc:view
  ...       name="index"
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="public protected"
  ...       class="zope.app.testing.xmlrpc.README.ProtectedView"
  ...       />
  ... </configure>
  ... """)

An unauthenticated user can access the public method, but not the protected
one:

  >>> proxy = ServerProxy("http://usr:usrpw@localhost/index", handleErrors=False)
  >>> proxy.public()
  'foo'
  >>> proxy.protected() # doctest: +NORMALIZE_WHITESPACE
  Traceback (most recent call last):
  zope.security.interfaces.Unauthorized: (<zope.app.publisher.xmlrpc.metaconfigure.ProtectedView object at 0x...>, 'protected', 'zope.ManageContent')

As a manager, we can access both:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/index")
  >>> proxy.public()
  'foo'
  >>> proxy.protected()
  'bar'

Handling errors with the ServerProxy
====================================

Our server proxy for functional testing also supports getting the original
errors from Zope by not handling the errors in the publisher:


  >>> class ExceptionDemo:
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def your_exception(self):
  ...         raise Exception("Something went wrong!")

Now we'll register it as a view:

  >>> from zope.configuration import xmlconfig
  >>> ignored = xmlconfig.string("""
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:xmlrpc="http://namespaces.zope.org/xmlrpc"
  ...     >
  ...   <!-- We only need to do this include in this example,
  ...        Normally the include has already been done for us. -->
  ...   <include package="zope.app.publisher.xmlrpc" file="meta.zcml" />
  ...
  ...   <xmlrpc:view
  ...       for="zope.site.interfaces.IFolder"
  ...       methods="your_exception"
  ...       class="zope.app.testing.xmlrpc.README.ExceptionDemo"
  ...       permission="zope.ManageContent"
  ...       />
  ... </configure>
  ... """)

Now, when we call it, we get an XML-RPC fault:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/")
  >>> proxy.your_exception()
  Traceback (most recent call last):
  xmlrpc.client.Fault: <Fault -1: 'Unexpected Zope exception: Exception: Something went wrong!'>

We can also give the parameter `handleErrors` to have the errors not be
handled:

  >>> proxy = ServerProxy("http://mgr:mgrpw@localhost/", handleErrors=False)
  >>> proxy.your_exception()
  Traceback (most recent call last):
  Exception: Something went wrong!
