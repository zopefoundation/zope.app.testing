=========
 CHANGES
=========

5.0 (2023-02-10)
================

- Add support for Python 3.8, 3.9, 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.


4.0.0 (2018-10-24)
==================

- Remove ``zope.app.testing.testbrowser``. It was not compatible with
  zope.testbrowser version 5.

- Add basic support for Python 3.5, 3.6 and 3.7.

3.10.0 (2012-01-13)
===================

- Removed test dependency on ``zope.app.authentication``.

  zope.testbrowser 4 depends on this change (seriously) if it find
  zope.app.testing.

3.9.0 (2011-03-14)
==================

- Move zope.app.testing testbrowser functionality into zope.app.testing. This
  requires zope.testbrowser version 4.0.0 or above.

3.8.1 (2011-01-07)
==================

- Include REMOTE_ADDR ('127.0.0.1') in the request environment.


3.8.0 (2010-09-14)
==================

- Remove invalid HTTP_REFERER default. (We both don't want a default to allow
  others testing without a referer and 'localhost' is not a reasonable
  default anyway.) This improves the situation for #98437

- Made the xmlrpc code compatible with Python 2.7.

- Removed test dependency on ``zope.app.zptpage``.

- Switched test dependency from ``zope.app.securitypolicy`` to
  ``zope.securitypolicy``.


3.7.7 (2010-09-14)
==================

- Rereleasing 3.7.5 as 3.7.7 to fix brown bag release.


3.7.6 (2010-09-14)
==================

- Brown bag release: It broke the tests of ``zope.testbrowser``.


3.7.5 (2010-04-10)
==================

- Switch doctests to use the stdlib ``doctest`` module, rather than the
  deprecated ``zope.testing.doctest`` variant.


3.7.4 (2010-01-08)
==================

- Import hooks functionality from zope.component after it was moved there from
  zope.site.

- Import ISite from zope.component after it was moved there from
  zope.location. This lifts the dependency on zope.location.

- Fix tests using a newer zope.publisher that requires zope.login.

3.7.3 (2009-08-20)
==================

- Fixed tests for python 2.4 as well as python 2.5 and 2.6; the change in
  version 3.7.1 introduced test regressions in python 2.4.

3.7.2 (2009-07-24)
==================

- Adjusted tests after the referenced memory leak problem has been fixed in
  ``zope.component``.


3.7.1 (2009-07-21)
==================

- Fixed failing tests. The code revealed that the tests expected the wrong
  value.


3.7.0 (2009-06-19)
==================

- Depend on new ``zope.processlifetime`` interfaces instead of using
  BBB imports from ``zope.app.appsetup``.

- Removed unused dependency on ``zope.app.component``.


3.6.2 (2009-04-26)
==================

- Removed deprecated back35 module and loose the dependency on
  ``zope.deferredimport``.

- Adapt to ``zope.app.authentication`` refactoring. We depend on
  ``zope.password`` now instead.

- Adapt to latest ``zope.app.security`` refactoring. We don't need this
  package anymore.

3.6.1 (2009-03-12)
==================

- Use ISkinnable.providedBy(request) instead of IBrowserRequest as condition
  for calling setDefaultSkin in HTTPCaller. This at the same time removes
  dependency to the browser part of zope.publisher.

- Adapt to the move of IDefaultViewName from zope.component.interfaces
  to zope.publisher.interfaces.

- Remove the DEPENDENCIES.cfg file for zpkg.

3.6.0 (2009-02-01)
==================

- Fix AttributeError in ``zope.app.testing.setup.setUpTestAsModule``
  (when called without name argument).

- Use ``zope.container`` instead of ``zope.app.container``.

- Use ``zope.site`` instead of ``zope.app.folder`` and
  ``zope.app.component`` for some parts.

3.5.6 (2008-10-13)
==================

- Change argument variable name in provideAdapter to not conflict with
  buitin keyword in Python 2.6.

3.5.5 (2008-10-10)
==================

- Re-configured functional test setup to create test-specific instances
  of HTTPCaller to ensure that cookies are not shared by doctests
  in a test suite.

3.5.4 (2008-08-25)
==================

- Clean up some transaction management in the functional test setup.

3.5.3 (2008-08-22)
==================

- Fix isolation enforcement for product configuration around individual tests.

3.5.2 (2008-08-21)
==================

- Added missing dependency information in setup.py.

- Added missing import.

- Repair memory leak fix released in 3.4.3 to be more sane in the presence of
  generations.

3.5.1 (2008-08-20)
==================

- Correct Fred's "I'm a doofus" release.

3.5.0 (2008-08-20)
==================

- Add support for product-configuration as part of functional layers; this
  more closely mirrors the configuration order for normal operation.

3.4.3 (2008-07-25)
==================

- Fix memory leak in all functional tests.
  see: https://bugs.launchpad.net/zope3/+bug/251273

3.4.2 (2008-02-02)
==================

- Fix of 599 error on conflict error in request
  see: http://mail.zope.org/pipermail/zope-dev/2008-January/030844.html

3.4.1 (2007-10-31)
==================

- Fixed deprecation warning for ``ZopeSecurityPolicy``.

3.4.0 (2007-10-27)
==================

- Initial release independent of the main Zope tree.
