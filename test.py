#! /usr/bin/env python2.3
##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""test.py [-abBcdDfFgGhklLmMPprstTuUv] [modfilter [testfilter...]]

Find and run tests written using the unittest module.

The test runner searches for Python modules that contain test suites.
It collects those suites, and runs the tests.  There are many options
for controlling how the tests are run.  There are options for using
the debugger, reporting code coverage, and checking for refcount problems.

The test runner uses the following rules for finding tests to run.  It
searches for packages and modules that contain "tests" as a component
of the name, e.g. "frob.tests.nitz" matches this rule because tests is
a sub-package of frob.  Within each "tests" package, it looks for
modules that begin with the name "test."  For each test module, it
imports the module and calls the module's test_suite() function, which must
return a unittest TestSuite object.

Options can be specified as command line arguments (see below). However,
options may also be specified in a file named 'test.config', a Python
script which, if found, will be executed before the command line
arguments are processed.

The test.config script should specify options by setting zero or more of the
global variables: LEVEL, BUILD, and other capitalized variable names found in
the test runner script (see the list of global variables in process_args().).


-a level
--at-level level
--all
    Run the tests at the given level.  Any test at a level at or below
    this is run, any test at a level above this is not run.  Level 0
    runs all tests.  The default is to run tests at level 1.  --all is
    a shortcut for -a 0.

-b
--build
    Run "python setup.py build" before running tests, where "python"
    is the version of python used to run test.py.  Highly recommended.
    Tests will be run from the build directory.

-B
--build-inplace
    Run "python setup.py build_ext -i" before running tests.  Tests will be
    run from the source directory.

-c
--pychecker
    use pychecker

-d
--debug
    Instead of the normal test harness, run a debug version which
    doesn't catch any exceptions.  This is occasionally handy when the
    unittest code catching the exception doesn't work right.
    Unfortunately, the debug harness doesn't print the name of the
    test, so Use With Care.

-D
--debug-inplace
    Works like -d, except that it loads pdb when an exception occurs.

--dir directory
-s directory
    Option to limit where tests are searched for. This is important
    when you *really* want to limit the code that gets run.  This can
    be specified more than once to run tests in two different parts of
    the source tree.
    For example, if refactoring interfaces, you don't want to see the way
    you have broken setups for tests in other packages. You *just* want to
    run the interface tests.

-f
--skip-unit
    Run functional tests but not unit tests.
    Note that functional tests will be skipped if the module
    zope.app.testing.functional cannot be imported.
    Functional tests also expect to find the file ftesting.zcml,
    which is used to configure the functional-test run.

-F
    DEPRECATED. Run both unit and functional tests.
    This option is deprecated, because this is the new default mode.
    Note that functional tests will be skipped if the module
    zope.app.testing.functional cannot be imported.

-g threshold
--gc-threshold threshold
    Set the garbage collector generation0 threshold.  This can be used
    to stress memory and gc correctness.  Some crashes are only
    reproducible when the threshold is set to 1 (agressive garbage
    collection).  Do "-g 0" to disable garbage collection altogether.

-G gc_option
--gc-option gc_option
    Set the garbage collection debugging flags.  The argument must be one
    of the DEBUG_ flags defined bythe Python gc module.  Multiple options
    can be specified by using "-G OPTION1 -G OPTION2."

-k
--keepbytecode
    Do not delete all stale bytecode before running tests

-l test_root
--libdir test_root
    Search for tests starting in the specified start directory
    (useful for testing components being developed outside the main
    "src" or "build" trees).

-L
--loop
    Keep running the selected tests in a loop.  You may experience
    memory leakage.

--module modfilter
    Provide a module filter (see modfilter below)

-N n
--repeat n
    Run the selected tests n times.

-m
-M  minimal GUI. See -U.

-P
--profile
    Run the tests under hotshot and display the top 50 stats, sorted by
    cumulative time and number of calls.

-p
--progress
    Show running progress.  It can be combined with -v or -vv.

-r
--refcount
    Look for refcount problems.
    This requires that Python was built --with-pydebug.

-1
--report-only-first-doctest-failure

   Report only the first failure in a doctest. (Examples after the
   failure are still executed, in case they do any cleanup.)

-t
--top-fifty
    Time the individual tests and print a list of the top 50, sorted from
    longest to shortest.

--test testfilter
    Provide a test filter (see testfilter below)

--times n
--times outfile
    With an integer argument, time the tests and print a list of the top <n>
    tests, sorted from longest to shortest.
    With a non-integer argument, specifies a file to which timing information
    is to be printed.

-T
--trace
    Use the trace module from Python for code coverage.  The current
    utility writes coverage files to a directory named `coverage' that
    is parallel to `build'.  It also prints a summary to stdout.

-u
--skip-functional
    CHANGED. Run unit tests but not functional tests.
    Note that the meaning of -u is changed from its former meaning,
    which is now specified by -U or --gui.

-U
--gui
    Use the PyUnit GUI instead of output to the command line.  The GUI
    imports tests on its own, taking care to reload all dependencies
    on each run.  The debug (-d), verbose (-v), progress (-p), and
    Loop (-L) options will be ignored.  The testfilter filter is also
    not applied.

-m
-M
--minimal-gui
    Note: -m is DEPRECATED in favour of -M or --minimal-gui.
    -m starts the gui minimized.  Double-clicking the progress bar
    will start the import and run all tests.


-v
--verbose
    Verbose output.  With one -v, unittest prints a dot (".") for each
    test run.  With -vv, unittest prints the name of each test (for
    some definition of "name" ...).  With no -v, unittest is silent
    until the end of the run, except when errors occur.

    When -p is also specified, the meaning of -v is slightly
    different.  With -p and no -v only the percent indicator is
    displayed.  With -p and -v the test name of the current test is
    shown to the right of the percent indicator.  With -p and -vv the
    test name is not truncated to fit into 80 columns and it is not
    cleared after the test finishes.


modfilter
testfilter...
    Case-sensitive regexps to limit which tests are run, used in search
    (not match) mode.
    In an extension of Python regexp notation, a leading "!" is stripped
    and causes the sense of the remaining regexp to be negated (so "!bc"
    matches any string that does not match "bc", and vice versa).
    By default these act like ".", i.e. nothing is excluded.

    modfilter is applied to a test file's path, starting at "build" and
    including (OS-dependent) path separators.  Additional modfilters
    can be specified with the --module option; modules are matched if
    they match at least one modfilter.

    testfilter is applied to the (method) name of the unittest methods
    contained in the test files whose paths modfilter matched.
    Additional testfilters can be specified with the --test option;
    methods are matched if they match at least one testfilter.

Extreme (yet useful) examples:

    test.py -vvb . "^testWriteClient$"

    Builds the project silently, then runs unittest in verbose mode on all
    tests whose names are precisely "testWriteClient".  Useful when
    debugging a specific test.

    test.py -vvb . "!^testWriteClient$"

    As before, but runs all tests whose names aren't precisely
    "testWriteClient".  Useful to avoid a specific failing test you don't
    want to deal with just yet.

    test.py -M . "!^testWriteClient$"

    As before, but now opens up a minimized PyUnit GUI window (only showing
    the progress bar).  Useful for refactoring runs where you continually want
    to make sure all tests still pass.

$Id$
"""
import gc
import logging
import os
import re
import pdb
import sys
import threading    # just to get at Thread objects created by tests
import time
import traceback
import unittest
import warnings

FTESTING = "ftesting.zcml"

def set_trace_doctest(stdin=sys.stdin, stdout=sys.stdout, trace=pdb.set_trace):
    sys.stdin = stdin
    sys.stdout = stdout
    trace()

pdb.set_trace_doctest = set_trace_doctest

from distutils.util import get_platform

PLAT_SPEC = "%s-%s" % (get_platform(), sys.version[0:3])

class ImmediateTestResult(unittest._TextTestResult):

    __super_init = unittest._TextTestResult.__init__
    __super_startTest = unittest._TextTestResult.startTest
    __super_printErrors = unittest._TextTestResult.printErrors

    def __init__(self, stream, descriptions, verbosity,
                 count=None, progress=False):
        self.__super_init(stream, descriptions, verbosity)
        self._progress = progress
        self._progressWithNames = False
        self.count = count
        self._testtimes = {}
        if progress and verbosity == 1:
            self.dots = False
            self._progressWithNames = True
            self._lastWidth = 0
            self._maxWidth = 80
            try:
                import curses
            except ImportError:
                pass
            else:
                curses.setupterm()
                self._maxWidth = curses.tigetnum('cols')
            self._maxWidth -= len("xxxx/xxxx (xxx.x%): ") + 1

    def stopTest(self, test):
        self._testtimes[test] = time.time() - self._testtimes[test]
        if gc.garbage:
            print "The following test left garbage:"
            print test
            print gc.garbage
            # TODO: Perhaps eat the garbage here, so that the garbage isn't
            #       printed for every subsequent test.

        # Did the test leave any new threads behind?
        new_threads = [t for t in threading.enumerate()
                         if (t.isAlive()
                             and
                             t not in self._threads)]
        if new_threads:
            print "The following test left new threads behind:"
            print test
            print "New thread(s):", new_threads

    def print_times(self, stream, count=None):
        results = self._testtimes.items()
        results.sort(lambda x, y: cmp(y[1], x[1]))
        if count:
            n = min(count, len(results))
            if n:
                print >>stream, "Top %d longest tests:" % n
        else:
            n = len(results)
        if not n:
            return
        for i in range(n):
            print >>stream, "%6dms" % int(results[i][1] * 1000), results[i][0]

    def _print_traceback(self, msg, err, test, errlist):
        if self.showAll or self.dots or self._progress:
            self.stream.writeln("\n")
            self._lastWidth = 0

        tb = "".join(traceback.format_exception(*err))
        self.stream.writeln(msg)
        self.stream.writeln(tb)
        errlist.append((test, tb))

    def startTest(self, test):
        if self._progress:
            self.stream.write("\r%4d" % (self.testsRun + 1))
            if self.count:
                self.stream.write("/%d (%5.1f%%)" % (self.count,
                                  (self.testsRun + 1) * 100.0 / self.count))
            if self.showAll:
                self.stream.write(": ")
            elif self._progressWithNames:
                # TODO: will break with multibyte strings
                name = self.getShortDescription(test)
                width = len(name)
                if width < self._lastWidth:
                    name += " " * (self._lastWidth - width)
                self.stream.write(": %s" % name)
                self._lastWidth = width
            self.stream.flush()
        self._threads = threading.enumerate()

        self.__super_startTest(test)
        # the super version can't count. ;)
        self.testsRun += test.countTestCases() - 1

        self._testtimes[test] = time.time()


    def getShortDescription(self, test):
        s = self.getDescription(test)
        if len(s) > self._maxWidth:
            pos = s.find(" (")
            if pos >= 0:
                w = self._maxWidth - (pos + 5)
                if w < 1:
                    # first portion (test method name) is too long
                    s = s[:self._maxWidth-3] + "..."
                else:
                    pre = s[:pos+2]
                    post = s[-w:]
                    s = "%s...%s" % (pre, post)
        return s[:self._maxWidth]

    def addError(self, test, err):
        if self._progress:
            self.stream.write("\r")
        self._print_traceback("Error in test %s" % test, err,
                              test, self.errors)

    def addFailure(self, test, err):
        if self._progress:
            self.stream.write("\r")
        self._print_traceback("Failure in test %s" % test, err,
                              test, self.failures)

    def printErrors(self):
        if VERBOSE < 2:
            # We'be output errors as they occured. Outputing them a second
            # time is just annoying. 
            return

        if self._progress and not (self.dots or self.showAll):
            self.stream.writeln()
        self.__super_printErrors()

    def printErrorList(self, flavor, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavor, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln(err)


class ImmediateTestRunner(unittest.TextTestRunner):

    __super_init = unittest.TextTestRunner.__init__

    def __init__(self, **kwarg):
        progress = kwarg.get("progress")
        if progress is not None:
            del kwarg["progress"]
        profile = kwarg.get("profile")
        if profile is not None:
            del kwarg["profile"]
        self.__super_init(**kwarg)
        self._progress = progress
        self._profile = profile
        # Create the test result here, so that we can add errors if
        # the test suite search process has problems.  The count
        # attribute must be set in run(), because we won't know the
        # count until all test suites have been found.
        self.result = ImmediateTestResult(
            self.stream, self.descriptions, self.verbosity,
            progress=self._progress)

    def _makeResult(self):
        # Needed base class run method.
        return self.result

    def run(self, test):
        self.result.count = test.countTestCases()
        if self._profile:
            import hotshot, hotshot.stats
            prof = hotshot.Profile("tests_profile.prof")
            args = (self, test)
            r = prof.runcall(unittest.TextTestRunner.run, *args)
            prof.close()
            stats = hotshot.stats.load("tests_profile.prof")
            stats.sort_stats('cumulative', 'calls')
            stats.print_stats(50)
            return r
        return unittest.TextTestRunner.run(self, test)

# setup list of directories to put on the path
class PathInit(object):
    def __init__(self, build, build_inplace, libdir=None):
        self.inplace = None
        # Figure out if we should test in-place or test in-build.  If the -b
        # or -B option was given, test in the place we were told to build in.
        # Otherwise, we'll look for a build directory and if we find one,
        # we'll test there, otherwise we'll test in-place.
        if build:
            self.inplace = build_inplace
        if self.inplace is None:
            # Need to figure it out
            if os.path.isdir(os.path.join("build", "lib.%s" % PLAT_SPEC)):
                self.inplace = False
            else:
                self.inplace = True
        # Calculate which directories we're going to add to sys.path, and cd
        # to the appropriate working directory
        self.org_cwd = os.getcwd()
        if self.inplace:
            self.libdir = "src"
        else:
            self.libdir = "lib.%s" % PLAT_SPEC
            os.chdir("build")
        # Hack sys.path
        self.cwd = os.getcwd()
        sys.path.insert(0, os.path.join(self.cwd, self.libdir))
        # Hack again for external products.
        kind = functional and "FUNCTIONAL" or "UNIT"
        if libdir:
            extra = os.path.join(self.org_cwd, libdir)
            print "Running %s tests from %s" % (kind, extra)
            self.libdir = extra
            sys.path.insert(0, extra)
        else:
            print "Running %s tests from %s" % (kind, self.cwd)

def match(rxlist, s):
    if not rxlist:
        return True
    for rx in rxlist:
        if rx[0] == "!":
            matched = re.search(rx[1:], s) is None
        else:
            matched = re.search(rx, s) is not None
        if matched:
            return True
    return False

class TestFileFinder(object):

    EMPTY_FILE_LISTS = ([], ["{arch}"], ["CVS"], ["_darcs"], [".svn"])

    def __init__(self, prefix):
        self.files = []
        self._plen = len(prefix)
        if not prefix.endswith(os.sep):
            self._plen += 1
        if functional:
            self.dirname = "ftests"
        else:
            self.dirname = "tests"

    def visit(self, rx, dir, files):
        if os.path.basename(dir) != self.dirname:
            # Allow tests/ftests module rather than package.
            modfname = self.dirname + '.py'
            if modfname in files:
                path = os.path.join(dir, modfname)
                if match(rx, path):
                    self.files.append(path)
                    return
            return
        # ignore tests that aren't in packages
        if "__init__.py" not in files:
            if files in self.EMPTY_FILE_LISTS:
                return
            print "not a package", dir
            return

        # Put matching files in matches.  If matches is non-empty,
        # then make sure that the package is importable.
        matches = []
        for file in files:
            if file.startswith('test') and os.path.splitext(file)[-1] == '.py':
                path = os.path.join(dir, file)
                if match(rx, path):
                    matches.append(path)

        # ignore tests when the package can't be imported, possibly due to
        # dependency failures.
        pkg = dir[self._plen:].replace(os.sep, '.')
        try:
            __import__(pkg)
        # We specifically do not want to catch ImportError since that's useful
        # information to know when running the tests.
        except RuntimeError, e:
            if VERBOSE:
                print "skipping %s because: %s" % (pkg, e)
            return
        else:
            self.files.extend(matches)

    def module_from_path(self, path):
        """Return the Python package name indicated by the filesystem path."""
        assert path.endswith(".py")
        path = path[self._plen:-3]
        mod = path.replace(os.sep, ".")
        return mod

def walk_with_symlinks(top, func, arg):
    """Like os.path.walk, but follows symlinks on POSIX systems.

    This could theoreticaly result in an infinite loop, if you create symlink
    cycles in your Zope sandbox, so don't do that.
    """
    try:
        names = os.listdir(top)
    except os.error:
        return
    exceptions = ('.', '..', '{arch}', '.arch-ids', '_darcs')
    names = [name for name in names
             if name not in exceptions
             if not name.startswith(',,')]
    func(arg, top, names)
    for name in names:
        name = os.path.join(top, name)
        if os.path.isdir(name):
            walk_with_symlinks(name, func, arg)

def find_test_dir(dir):
    if os.path.exists(dir):
        return dir
    d = os.path.join(pathinit.libdir, dir)
    if os.path.exists(d):
        if os.path.isdir(d):
            return d
        raise ValueError("%s does not exist and %s is not a directory"
                         % (dir, d))
    raise ValueError("%s does not exist!" % dir)

def find_tests(rx):
    global finder
    finder = TestFileFinder(pathinit.libdir)

    if TEST_DIRS:
        for d in TEST_DIRS:
            d = find_test_dir(d)
            walk_with_symlinks(d, finder.visit, rx)
    else:
        walk_with_symlinks(pathinit.libdir, finder.visit, rx)
    return finder.files

def package_import(modname):
    __import__(modname)
    return sys.modules[modname]

class PseudoTestCase(object):
    """Minimal test case objects to create error reports.

    If test.py finds something that looks like it should be a test but
    can't load it or find its test suite, it will report an error
    using a PseudoTestCase.
    """

    def __init__(self, name, descr=None):
        self.name = name
        self.descr = descr

    def shortDescription(self):
        return self.descr

    def __str__(self):
        return "Invalid Test (%s)" % self.name

def get_suite(file, result=None):
    modname = finder.module_from_path(file)
    try:
        mod = package_import(modname)
        return mod.test_suite()
    except:
        if result is not None:
            result.addError(PseudoTestCase(modname), sys.exc_info())
            return None
        raise

def filter_testcases(s, rx):
    new = unittest.TestSuite()
    for test in s._tests:
        # See if the levels match
        dolevel = (LEVEL == 0) or LEVEL >= getattr(test, "level", 0)
        if not dolevel:
            continue
        if isinstance(test, unittest.TestCase):
            name = test.id() # Full test name: package.module.class.method
            name = name[1 + name.rfind("."):] # extract method name
            if not rx or match(rx, name):
                new.addTest(test)
        else:
            filtered = filter_testcases(test, rx)
            if filtered:
                new.addTest(filtered)
    return new

def gui_runner(files, test_filter):
    if BUILD_INPLACE:
        utildir = os.path.join(os.getcwd(), "utilities")
    else:
        utildir = os.path.join(os.getcwd(), "..", "utilities")
    sys.path.append(utildir)
    import unittestgui
    suites = []
    for file in files:
        suites.append(finder.module_from_path(file) + ".test_suite")

    suites = ", ".join(suites)
    minimal = (GUI == "minimal")
    unittestgui.main(suites, minimal)

class TrackRefs(object):
    """Object to track reference counts across test runs."""

    def __init__(self):
        self.type2count = {}
        self.type2all = {}

    def update(self):
        obs = sys.getobjects(0)
        type2count = {}
        type2all = {}
        for o in obs:
            all = sys.getrefcount(o)

            if type(o) is str and o == '<dummy key>':
                # avoid dictionary madness
                continue
            t = type(o)
            if t in type2count:
                type2count[t] += 1
                type2all[t] += all
            else:
                type2count[t] = 1
                type2all[t] = all

        ct = [(type2count[t] - self.type2count.get(t, 0),
               type2all[t] - self.type2all.get(t, 0),
               t)
              for t in type2count.iterkeys()]
        ct.sort()
        ct.reverse()
        printed = False
        for delta1, delta2, t in ct:
            if delta1 or delta2:
                if not printed:
                    print "%-55s %8s %8s" % ('', 'insts', 'refs')
                    printed = True
                print "%-55s %8d %8d" % (t, delta1, delta2)

        self.type2count = type2count
        self.type2all = type2all

def print_doctest_location(err):
    # This mimicks pdb's output, which gives way cool results in emacs :)
    filename = err.test.filename
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    print "> %s(%s)_()" % (filename, err.test.lineno+err.example.lineno+1)

def post_mortem(exc_info):
    from zope.testing import doctest
    err = exc_info[1]
    if isinstance(err, (doctest.UnexpectedException, doctest.DocTestFailure)):

        if isinstance(err, doctest.UnexpectedException):
            exc_info = err.exc_info

            # Print out location info if the error was in a doctest
            if exc_info[2].tb_frame.f_code.co_filename == '<string>':
                print_doctest_location(err)
            
        else:
            print_doctest_location(err)
            # Hm, we have a DocTestFailure exception.  We need to
            # generate our own traceback
            try:
                exec ('raise ValueError'
                      '("Expected and actual output are different")'
                      ) in err.test.globs
            except:
                exc_info = sys.exc_info()
        
    print "%s:" % (exc_info[0], )
    print exc_info[1]
    pdb.post_mortem(exc_info[2])
    sys.exit()

def run_debug(test_or_suite, verbosity):
    if isinstance(test_or_suite, unittest.TestCase):
        # test
        if verbosity > 1:
            print test_or_suite
        elif verbosity > 0:
            print '.',

        try:
            test_or_suite.debug()
        except:
            if DEBUGGER:
                post_mortem(sys.exc_info())
            raise
        return 1

    else:
        r = 0
        for t in test_or_suite._tests: # Ick _tests
            r += run_debug(t, verbosity)
        return r
            
def runner(files, test_filter, debug):

    if DEBUG:
        runner = result = None 
    else:
        runner = ImmediateTestRunner(verbosity=VERBOSE,
                                     progress=PROGRESS, profile=PROFILE,
                                     descriptions=False)
        result = runner.result

    suite = unittest.TestSuite()
    for file in files:
        try:
            s = get_suite(file, result)
        except:
            if DEBUGGER:
                post_mortem(sys.exc_info())
            raise
            
        # See if the levels match
        dolevel = (LEVEL == 0) or LEVEL >= getattr(s, "level", 0)
        if s is not None and dolevel:
            s = filter_testcases(s, test_filter)
            suite.addTest(s)

    if DEBUG:
        print "Ran %s tests in debug mode" % run_debug(suite, VERBOSE)
        return 0

    r = runner.run(suite)
    if TIMESFN:
        r.print_times(open(TIMESFN, "w"))
        if VERBOSE:
            print "Wrote timing data to", TIMESFN
    if TIMETESTS:
        r.print_times(sys.stdout, TIMETESTS)
    numbad = len(result.failures) + len(result.errors)
    return numbad

def remove_stale_bytecode(arg, dirname, names):
    names = map(os.path.normcase, names)
    for name in names:
        if name.endswith(".pyc") or name.endswith(".pyo"):
            srcname = name[:-1]
            if srcname not in names:
                fullname = os.path.join(dirname, name)
                print "Removing stale bytecode file", fullname
                os.unlink(fullname)

def main(module_filter, test_filter, libdir):
    if not KEEP_STALE_BYTECODE:
        os.path.walk(os.curdir, remove_stale_bytecode, None)

    configure_logging()

    # Initialize the path and cwd
    global pathinit
    pathinit = PathInit(BUILD, BUILD_INPLACE, libdir)

    files = find_tests(module_filter)
    if not files:
        print ("No %s tests to be run."
               % (functional and "functional" or "unit"))
        return
    files.sort()

    # Make sure functional tests find ftesting.zcml
    if functional:
        config_file = FTESTING
        if not pathinit.inplace:
            # We chdired into build, so ftesting.zcml is in the
            # parent directory
            config_file = os.path.join('..', FTESTING)
        print "Parsing %s" % config_file
        from zope.app.testing.functional import FunctionalTestSetup
        FunctionalTestSetup(config_file)

    numbad = 0
    if GUI:
        gui_runner(files, test_filter)
    elif LOOP:
        if REFCOUNT:
            rc = sys.gettotalrefcount()
            track = TrackRefs()

        n = LOOP
        i = 1
        while i <= n:
            print
            print "Run %s:" % i
            i += 1;
            numbad = runner(files, test_filter, DEBUG)
            gc.collect()
            if gc.garbage:
                print "GARBAGE:", len(gc.garbage), gc.garbage
                return numbad

            if REFCOUNT:
                prev = rc
                rc = sys.gettotalrefcount()
                print "totalrefcount=%-8d change=%-6d" % (rc, rc - prev)
                track.update()
    else:
        numbad = runner(files, test_filter, DEBUG)

    os.chdir(pathinit.org_cwd)
    return numbad


def configure_logging():
    """Initialize the logging module."""
    import logging.config

    # Get the log.ini file from the current directory instead of possibly
    # buried in the build directory.
    # TODO: This isn't perfect because if log.ini specifies a log file, it'll be
    # relative to the build directory.
    # Hmm...
    logini = os.path.abspath("log.ini")

    if os.path.exists(logini):
        logging.config.fileConfig(logini)
    else:
        # If there's no log.ini, cause the logging package to be
        # silent during testing.
        root = logging.getLogger()
        root.addHandler(NullHandler())
        logging.basicConfig()

    if os.environ.has_key("LOGGING"):
        level = int(os.environ["LOGGING"])
        logging.getLogger().setLevel(level)


class NullHandler(logging.Handler):
    """Logging handler that drops everything on the floor.

    We require silence in the test environment.  Hush.
    """

    def emit(self, record):
        pass


def process_args(argv=None):
    import getopt
    global MODULE_FILTER
    global TEST_FILTER
    global VERBOSE
    global LOOP
    global GUI
    global TRACE
    global REFCOUNT
    global DEBUG
    global DEBUGGER
    global BUILD
    global LEVEL
    global LIBDIR
    global TIMESFN
    global TIMETESTS
    global PROGRESS
    global BUILD_INPLACE
    global KEEP_STALE_BYTECODE
    global TEST_DIRS
    global PROFILE
    global GC_THRESHOLD
    global GC_FLAGS
    global RUN_UNIT
    global RUN_FUNCTIONAL
    global PYCHECKER
    global REPORT_ONLY_FIRST_DOCTEST_FAILURE

    if argv is None:
        argv = sys.argv

    MODULE_FILTERS = []
    TEST_FILTERS = []
    VERBOSE = 0
    LOOP = 0
    GUI = False
    TRACE = False
    REFCOUNT = False
    DEBUG = False # Don't collect test results; simply let tests crash
    DEBUGGER = False
    BUILD = False
    BUILD_INPLACE = False
    GC_THRESHOLD = None
    gcdebug = 0
    GC_FLAGS = []
    LEVEL = 1
    LIBDIR = None
    PROGRESS = False
    TIMESFN = None
    TIMETESTS = 0
    KEEP_STALE_BYTECODE = 0
    RUN_UNIT = True
    RUN_FUNCTIONAL = True
    TEST_DIRS = []
    PROFILE = False
    PYCHECKER = False
    REPORT_ONLY_FIRST_DOCTEST_FAILURE = False
    config_filename = 'test.config'

    # import the config file
    if os.path.isfile(config_filename):
        print 'Configuration file found.'
        execfile(config_filename, globals())


    try:
        opts, args = getopt.gnu_getopt(argv[1:],
                                   "a:bBcdDfFg:G:hkl:LmMPprs:tTuUvN:1",
                                   ["all", "help", "libdir=", "times=",
                                    "keepbytecode", "dir=", "build",
                                    "build-inplace",
                                    "at-level=",
                                    "pychecker", "debug", "pdebug",
                                    "gc-threshold=", "gc-option=",
                                    "loop", "gui", "minimal-gui",
                                    "test=", "module=",
                                    "profile", "progress", "refcount", "trace",
                                    "top-fifty", "verbose", "repeat=",
                                    "report-only-first-doctest-failure",
                                    ])
    # fixme: add the long names
    # fixme: add the extra documentation
    # fixme: test for functional first!
    except getopt.error, msg:
        print msg
        print "Try `python %s -h' for more information." % argv[0]
        sys.exit(2)

    for k, v in opts:
        if k in ("-a", "--at-level"):
            LEVEL = int(v)
        elif k == "--all":
            LEVEL = 0
            os.environ["COMPLAIN_IF_TESTS_MISSED"]='1'
        elif k in ("-b", "--build"):
            BUILD = True
        elif k in ("-B", "--build-inplace"):
            BUILD = BUILD_INPLACE = True
        elif k in("-c", "--pychecker"):
            PYCHECKER = True
        elif k in ("-d", "--debug"):
            DEBUG = True
        elif k in ("-D", "--pdebug"):
            DEBUG = True
            DEBUGGER = True
        elif k in ("-f", "--skip-unit"):
            RUN_UNIT = False
        elif k in ("-u", "--skip-functional"):
            RUN_FUNCTIONAL = False
        elif k == "-F":
            message = 'Unit plus functional is the default behaviour.'
            warnings.warn(message, DeprecationWarning)
            RUN_UNIT = True
            RUN_FUNCTIONAL = True
        elif k in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif k in ("-g", "--gc-threshold"):
            GC_THRESHOLD = int(v)
        elif k in ("-G", "--gc-option"):
            if not v.startswith("DEBUG_"):
                print "-G argument must be DEBUG_ flag, not", repr(v)
                sys.exit(1)
            GC_FLAGS.append(v)
        elif k in ('-k', '--keepbytecode'):
            KEEP_STALE_BYTECODE = 1
        elif k in ('-l', '--libdir'):
            LIBDIR = v
        elif k in ("-L", "--loop"):
            LOOP = 1000000000
        elif k in ("-N", "--repeat"):
            LOOP = int(v)
        elif k == "-m":
            GUI = "minimal"
            msg = "Use -M or --minimal-gui instead of -m."
            warnings.warn(msg, DeprecationWarning)
        elif k in ("-M", "--minimal-gui"):
            GUI = "minimal"
        elif k in ("-P", "--profile"):
            PROFILE = True
        elif k in ("-p", "--progress"):
            PROGRESS = True
        elif k in ("-r", "--refcount"):
                REFCOUNT = True
        elif k in ("-T", "--trace"):
            TRACE = True
        elif k in ("-t", "--top-fifty"):
            if not TIMETESTS:
                TIMETESTS = 50
        elif k in ("-U", "--gui"):
            GUI = 1
        elif k in ("-1", "--report-only-first-doctest-failure"):
            REPORT_ONLY_FIRST_DOCTEST_FAILURE = True
        elif k in ("-v", "--verbose"):
            VERBOSE += 1
        elif k == "--times":
            try:
                TIMETESTS = int(v)
            except ValueError:
                # must be a filename to write
                TIMESFN = v
        elif k in ('-s', '--dir'):
            TEST_DIRS.append(v)
        elif k == "--test":
            TEST_FILTERS.append(v)
        elif k == "--module":
            MODULE_FILTERS.append(v)

    if PYCHECKER:
        # make sure you have a recent version of pychecker
        if not os.environ.get("PYCHECKER"):
            os.environ["PYCHECKER"] = "-q"
        import pychecker.checker

    if REFCOUNT and not hasattr(sys, "gettotalrefcount"):
        print "-r ignored, because it needs a debug build of Python"
        REFCOUNT = False

    if sys.version_info < ( 2,3,4 ):
        print """\
        ERROR: Your python version is not supported by Zope3.
        Zope3 needs Python 2.3.4 or greater. You are running:""" + sys.version
        sys.exit(1)

    if REPORT_ONLY_FIRST_DOCTEST_FAILURE:
        import zope.testing.doctest
        zope.testing.doctest.set_unittest_reportflags(
            zope.testing.doctest.REPORT_ONLY_FIRST_FAILURE)
        import doctest
        if hasattr(doctest, 'REPORT_ONLY_FIRST_FAILURE'):
            doctest.set_unittest_reportflags(doctest.REPORT_ONLY_FIRST_FAILURE)

    if GC_THRESHOLD is not None:
        if GC_THRESHOLD == 0:
            gc.disable()
            print "gc disabled"
        else:
            gc.set_threshold(GC_THRESHOLD)
            print "gc threshold:", gc.get_threshold()

    if GC_FLAGS:
        val = 0
        for flag in GC_FLAGS:
            v = getattr(gc, flag, None)
            if v is None:
                print "Unknown gc flag", repr(flag)
                print gc.set_debug.__doc__
                sys.exit(1)
            val |= v
        gcdebug |= v

    if gcdebug:
        gc.set_debug(gcdebug)

    if BUILD:
        # Python 2.3 is more sane in its non -q output
        if sys.hexversion >= 0x02030000:
            qflag = ""
        else:
            qflag = "-q"
        cmd = sys.executable + " setup.py " + qflag + " build"
        if BUILD_INPLACE:
            cmd += "_ext -i"
        if VERBOSE:
            print cmd
        sts = os.system(cmd)
        if sts:
            print "Build failed", hex(sts)
            sys.exit(1)

    k = []
    if RUN_UNIT:
        k.append(False)
    if RUN_FUNCTIONAL:
        k.append(True)

    global functional
    numbad = 0
    for functional in k:

        if VERBOSE:
            kind = functional and "FUNCTIONAL" or "UNIT"
            if LEVEL == 0:
                print "Running %s tests at all levels" % kind
            else:
                print "Running %s tests at level %d" % (kind, LEVEL)

# This was to avoid functional tests outside of z3, but this doesn't really
# work right.
##         if functional:
##             try:
##                 from zope.app.testing.functional import FunctionalTestSetup
##             except ImportError:
##                 raise
##                 print ('Skipping functional tests: could not import '
##                        'zope.app.testing.functional')
##                 continue

        # TODO: We want to change *visible* warnings into errors.  The next
        # line changes all warnings into errors, including warnings we
        # normally never see.  In particular, test_datetime does some
        # short-integer arithmetic that overflows to long ints, and, by
        # default, Python doesn't display the overflow warning that can
        # be enabled when this happens.  The next line turns that into an
        # error instead.  Guido suggests that a better to get what we're
        # after is to replace warnings.showwarning() with our own thing
        # that raises an error.
        ## warnings.filterwarnings("error")
        warnings.filterwarnings("ignore", module="logging")

        if args:
            if len(args) > 1:
                TEST_FILTERS.extend(args[1:])
            MODULE_FILTERS.append(args[0])
        try:
            if TRACE:
                # if the trace module is used, then we don't exit with
                # status if on a false return value from main.
                coverdir = os.path.join(os.getcwd(), "coverage")
                import trace
                ignoremods = ["os", "posixpath", "stat"]
                tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix],
                                     ignoremods=ignoremods,
                                     trace=False, count=True)

                # we don't get the result from main() from runctx()
                tracer.runctx("main(MODULE_FILTERS, TEST_FILTERS, LIBDIR)",
                              globals=globals(), locals=vars())
                r = tracer.results()
                path = "/tmp/trace.%s" % os.getpid()
                import cPickle
                f = open(path, "wb")
                cPickle.dump(r, f)
                f.close()
                print path
                r.write_results(show_missing=True,
                                summary=True, coverdir=coverdir)
            else:
                bad = main(MODULE_FILTERS, TEST_FILTERS, LIBDIR)
                if bad:
                    numbad += bad
        except ImportError, err:
            print err
            print sys.path
            raise

    if numbad:
        sys.exit(1)


def test_suite():
    """Return an empty test suite to avoid complaints about this
    module not having a 'test_suite' attribute."""
    return unittest.TestSuite()


if __name__ == "__main__":
    process_args()
