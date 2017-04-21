idsFree
=======

*idsFree: automatic hacking for docketized applications, escaping to the Intrusion Detection Systems*

.. image::  https://github.com/bbva/idsfree/raw/master/doc/source/_static/idsfree-logo-256.png
    :height: 64px
    :width: 64px
    :alt: idsFree logo

.. image:: https://travis-ci.org/bbva/idsfree.svg?branch=master
    :target: https://travis-ci.org/bbva/idsfree

.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://github.com/bbva/idsfree/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/status/Django.svg
    :target: https://pypi.python.org/pypi/idsfree/1.0.0

.. image:: https://codecov.io/gh/bbva/idsfree/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bbva/idsfree

.. image:: https://readthedocs.org/projects/bbva/badge/?version=latest
    :target: http://idsfree.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

+----------------+--------------------------------------------+
|Project site    | https://github.com/bbva/idsfree            |
+----------------+--------------------------------------------+
|Issues          | https://github.com/bbva/idsfree/issues/    |
+----------------+--------------------------------------------+
|Documentation   | https://idsfree.readthedocs.io/            |
+----------------+--------------------------------------------+
|Authors         | Daniel Garcia (cr0hn)                      |
+----------------+--------------------------------------------+
|Latest Version  | 1.0.0-alpha                                |
+----------------+--------------------------------------------+
|Python versions | 3.5 or above                               |
+----------------+--------------------------------------------+

What's idsFree?
===============

This project try to launch hacking test without raise alerts into IDS
mechanisms.

The main problem when we try to do hacking for our own websites, and when we haven't infrastructure in other place but in cloud system (AWS, Google Compute engine, Digital Ocean, etc...) is that these providers doesn't allow to run hacking tools (even the applications are we own!).

To avoid this issue, we have created **idsFree**.

How it works?
=============

IdsFree get your application image (as a Docker image) and creates a Docker container using it. Then it connect the container to another docker container with hacking tools using a cyphered SDN and then: creating a **private**, **isolated** and **cyphered network** for your tests, in a **specified machine with SSH access**.

Then idsFree launch your hacking tests over your application, get the results and export it in a readable format (currently in JSON and XML JUnit format).

When test was ended, idsFree remove the containers, the private networks and clean the environment.

Quick start
===========

Install
-------

.. code-block:: bash

    > python3.5 -m pip install idsfree

Check remote environment
------------------------

IdsFree allow to check if a remote system has all the necessary conditions
to run. An examples of usage are:

**Check remote system by passing the password in command line**

.. code-block:: bash

    > idsfree -v -H 192.168.111.129  -d -U root -P MY_PASSWORD prepare
    [ * ] Starting preparation of remote host...
    [ * ] Checking remote machine for minimum requisites
    [ * ] Initialization Swarm at IP: 192.168.111.129
    [ * ] Creating new encrypted network: DgJXoXmeYhASHjmSV

**Check remote system and tell to idsFree ask for the password**

.. code-block:: bash

    > idsfree -v -H 192.168.111.129  -d -U root -A prepare
    [ * ] Starting preparation of remote host...
    [ * ] Checking remote machine for minimum requisites
    [ * ] Initialization Swarm at IP: 192.168.111.129
    [ * ] Creating new encrypted network: DgJXoXmeYhASHjmSV

Launching the attacks
---------------------

Currently, idsFree can launch two type of attacks: net | web, and try to
choice the best tools to perform the attacks.

Also, idsFree can report in two formats: **JSON** and **JUnit**.

**Launch attack and report in JUnit**

.. code-block:: bash

    > idsfree -v -H 192.168.111.129  -d -U root -P MY_PASSWORD run_attacks  -p  6379 -t net -s redis redis -o results.xml -e junit
    [ * ] Starting attacks of remote host...
    [ * ] Checking remote machine for minimum requisites
    [ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
    [ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
    [ * ] Generating results as 'JUnit' format, in file: 'results.xml'

**Launch attack, report in JSON and ask for password**

.. code-block:: bash

    > idsfree -v -H 192.168.111.129  -d -U root -A run_attacks  -p  6379 -t  net -s redis redis -o results.json -e json
    [ * ] Starting attacks of remote host...
    [ * ] Checking remote machine for minimum requisites
    [ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
    [ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
    [ * ] Generating results as 'json' format, in file: 'results.json'

Documentation
=============

(Still pending!)

Go to documentation site: https://idsfree.readthedocs.io/

Contributors
------------

Contributors are welcome. You can find a list ot TODO tasks in the `TODO.md
<https://github.com/bbva/idsfree/blob/master/TODO.md>`_ at the project file.

All contributors will be added to the `CONTRIBUTORS.md
<https://github.com/bbva/idsfree/blob/master/CONTRIBUTORS.md>`_ file.

Thanks in advance if you're planning to contribute to the project! :)

License
=======

This project is distributed under `BSD license <https://github.com/bbva/idsfree/blob/master/LICENSE>`_

