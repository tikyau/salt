# -*- coding: utf-8 -*-
'''
Memcache "Salt DB" Module

:maintainer:    SaltStack
:maturity:      New
:depends:       python-memcached
:platform:      all

This module allows access to memcache using an ``sdb://`` URI. This
package is located at ``https://pypi.python.org/pypi/python-memcached``.

Like all sdb modules, the memcache module requires a configuration profile to
be configured in either the minion or master configuration file. This profile
requires very little. In the example:

.. code-block:: yaml

    mymemcache:
      driver: memcache
      host: localhost
      port: 11211

The ``driver`` refers to the memcache module, ``host`` and ``port`` the
memcache server to connect to (defaults to ``localhost`` and ``11211``,
and ``mymemcache`` refers to the name that will appear in the URI:

.. code-block:: yaml

    password: sdb://mymemcache/mykey

'''

# import python libs
from __future__ import absolute_import
import logging

# import Salt libs
import salt.utils.memcache

# import third party libs
try:
    import memcache
    HAS_MEMCACHE = True
except ImportError:
    HAS_MEMCACHE = False

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 11211
DEFAULT_EXPIRATION = 0

log = logging.getLogger(__name__)

__func_alias__ = {
    'set_': 'set'
}

__virtualname__ = 'memcache'


def __virtual__():
    '''
    Only load the module if memcache is installed
    '''
    if HAS_MEMCACHE:
        return __virtualname__
    return False


def set_(key, value, profile=None):
    '''
    Set a key/value pair in memcached
    '''
    conn = salt.utils.memcache.get_conn(profile)
    time = profile.get('expire', DEFAULT_EXPIRATION)
    return salt.utils.memcache.set_(conn, key, value, time=time)


def get(key, profile=None):
    '''
    Get a value from memcached
    '''
    conn = salt.utils.memcache.get_conn(profile)
    return salt.utils.memcache.get(conn, key)
