===================
 FDocTest (How-To)
===================

Steps to get started:

1. Use a clean/missing Data.fs

2. Create a manager with the name "mgr", password "mgrpw", and grant
   the zope.Manager role.

3. Install tcpwatch.

4. Create a temporary directory to record tcpwatch output.

5. Run tcpwatch using:
   tcpwatch.py -L 8081:8080 -s -r tmpdir
   (the ports are the listening port and forwarded-to port; the
   second need to match the Zope configuration)

6. In a browser, connect to the listening port and do whatever needs
   to be recorded.

7. Shut down tcpwatch.

8. Run the script src/zope/app/testing/dochttp.py:
   python2.4 src/zope/app/testing/dochttp.py tmpdir > somefile.txt

9. Edit the generated text file to add explanations and elide
   uninteresting portions of the output.

10. In a functional test module (usually ftests.py), import
    FunctionalDocFileSuite from zope.app.testing.functional and
    instantiate it, passing the name of the text file containing
    the test.
