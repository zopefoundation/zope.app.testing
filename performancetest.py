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
""" Performance checker, see performancetest.txt
$Id:$
"""
from test import pystone
import time

# TOLERANCE in Pystones
TOLERANCE = 1000

class DurationError(AssertionError): pass

def local_pystone():
    return pystone.pystones(loops=pystone.LOOPS)

def timedtest(max_num_pystones, current_pystone=local_pystone()):
    """ decorator timedtest """
    if not isinstance(max_num_pystones, float):
        max_num_pystones = float(max_num_pystones)

    def _timedtest(function):
        def wrapper(*args, **kw):
            start_time = time.time()
            try:
                return function(*args, **kw)
            finally:
                total_time = time.time() - start_time
                if total_time == 0:
                    pystone_total_time = 0
                else:
                    pystone_rate = current_pystone[0] / current_pystone[1]
                    pystone_total_time = total_time / pystone_rate
                if pystone_total_time > (max_num_pystones + TOLERANCE):
                    raise DurationError((('Test too long (%.2f Ps, '
                                        'need at most %.2f Ps)')
                                        % (pystone_total_time,
                                            max_num_pystones)))
        return wrapper

    return _timedtest

def wtimedtest(func, max_num_pystones, current_pystone=local_pystone()):
    """ wrapper wtimedtest """
    if not isinstance(max_num_pystones, float):
        max_num_pystones = float(max_num_pystones)

    def wrapper(*args, **kw):
        start_time = time.time()
        try:
            return func(*args, **kw)
        finally:
            total_time = time.time() - start_time
            if total_time == 0:
                pystone_total_time = 0
            else:
                pystone_rate = current_pystone[0] / current_pystone[1]
                pystone_total_time = total_time / pystone_rate
            if pystone_total_time > (max_num_pystones + TOLERANCE):
                raise DurationError((('Test too long (%.2f Ps, '
                                    'need at most %.2f Ps)')
                                    % (pystone_total_time,
                                        max_num_pystones)))
    return wrapper
