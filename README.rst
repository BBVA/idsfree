idsFree
=======

*idsFree: automatic hacking for docketized applications, escaping to the Intrusion Detection Systems*

.. image::  https://github.com/cr0hn/idsfree/raw/master/doc/source/_static/idsfree-logo-256.png
    :height: 64px
    :width: 64px
    :alt: idsFree logo

.. image:: https://travis-ci.org//cr0hn/idsfree.svg?branch=master
    :target: https://travis-ci.org/cr0hn/idsfree

.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://github.com/cr0hn/idsfree/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/status/Django.svg
    :target: https://pypi.python.org/pypi/idsfree/1.0.0

.. image:: https://codecov.io/gh//cr0hn/idsfree/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/cr0hn/idsfree

.. image:: https://readthedocs.org/projects/cr0hn/badge/?version=latest
    :target: http://idsfree.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

+----------------+--------------------------------------------+
|Project site    | https://github.com/cr0hn/idsfree           |
+----------------+--------------------------------------------+
|Issues          | https://github.com/cr0hn/idsfree/issues/   |
+----------------+--------------------------------------------+
|Documentation   | https://idsfree.readthedocs.io/            |
+----------------+--------------------------------------------+
|Authors         | Daniel Garcia (cr0hn)                      |
+----------------+--------------------------------------------+
|Latest Version  | 1.0.0-alpha                                |
+----------------+--------------------------------------------+
|Python versions | 3.5 or above                               |
+----------------+--------------------------------------------+

What's idsFree
==============

This project try to launch hacking test without raise alerts into IDS
mechanisms.

The main problem when we try to do hacking for our own websites, and when we
 haven't infrastructure in other place but in cloud system (AWS, Google
 Compute engine, Digital Ocean, etc...) is that these providers doesn't allow
  to run hacking tools (even the applications are we own!).

To avoid this issue, we have created **idsFree**.

How it's works?
===============

IdsFree get your application image (as a Docker image) and creates a Docker
container using it. Then it connect the container to another docker container
with hacking tools using a cyphered SDN and then: creating a **private**,
**isolated** and **cyphered network** for your tests, in a **specified machine
with
SSH access**.

Then idsFree launch your hacking tests over your application, get the
results and export it in a readable format (currently in JSON and XML JUnit
format).

When test was ended, idsFree remove the containers, the private networks and
 clean the environment.

Documentation
=============

Go to documentation site: https://idsfree.readthedocs.io/

Contributors
------------

Contributors are welcome. You can find a list ot TODO tasks in the `TODO.md
<https://github.com/cr0hn/idsfree/blob/master/TODO.md>`_ at the project file.

All contributors will be added to the `CONTRIBUTORS.md
<https://github.com/cr0hn/idsfree/blob/master/CONTRIBUTORS.md>`_ file.

Thanks in advance if you're planning to contribute to the project! :)

License
=======

This project is distributed under `BSD license <https://github.com/cr0hn/idsfree/blob/master/LICENSE>`_

