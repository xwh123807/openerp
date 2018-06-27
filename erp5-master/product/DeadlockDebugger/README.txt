================
DeadlockDebugger
================

*$Id: README.txt,v 1.1 2005/02/23 15:35:21 fguillaume Exp $*

This product adds a hook so that a deadlocked Zope process can be
debugged, by dumping a traceback of all running python processes. The
dump is sent to the event log (at the DEBUG level) and returned to the
browser (even though the Zope is deadlocked and doesn't answer any
other requests!).

DeadlockDebugger can of course also be used in non-deadlock situations,
when a Zope process is taking a long time and you wish to know what code
is being executed.

Configuration
-------------

You must edit your zope.conf file and add product configuration:

<product-config deadlockdebugger>
  dump_url /manage_debug_threads
  secret mysecretkey
</product-config>

secret is optional.

Usage
-----

The standard way to call it is to go to the URL::

  http://yourzopesite:8080/manage_debug_threads?yoursecret

This will return a dump, and also send this dump to the event log.

A secret is needed because Zope doesn't do any access control on the URL
(it is intercepted too early), and the thread traceback dump may return
sensitive information about the requests being executed. If you know
your Zope will only be accessed by authorized persons anyway, you can
set secret to the empty string, and just call::

  http://yourzopesite:8080/manage_debug_threads

In any case you should filter out 'manage_debug_threads' in your
front-end proxy.

Credits
-------

This product is sponsored by Nuxeo <http://nuxeo.com>.

Please contact Florent Guillaume <fg@nuxeo.com> for problems.
You can use the zope@zope.org mailing-list to discuss this product.
