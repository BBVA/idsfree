idsFree
=======

*IdsFree: Launch hacking tests in cloud providers securely, isolated and without raise security alerts in the provider*

.. image::  https://raw.githubusercontent.com/BBVA/idsfree/master/docs/assets/images/idsfree-logo-256.png
    :height: 64px
    :width: 64px
    :alt: idsFree logo

.. image:: https://travis-ci.org/BBVA/idsfree.svg?branch=master
    :target: https://travis-ci.org/bbva/idsfree

.. image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://github.com/bbva/idsfree/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/status/Django.svg
    :target: https://pypi.python.org/pypi/idsfree/1.0.0

.. image:: https://codecov.io/gh/bbva/idsfree/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bbva/idsfree

.. image:: https://readthedocs.org/projects/idsfree/badge/?version=latest
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

**IdsFree** allow you to perform hacking testing without raise alerts at IDS mechanism.

What problem solve IdsFree?
===========================

There're many organizations and companies (an users too) that only have Cloud provides as an infrastructure for their own products, developments and any other thing that they will need.

But, **what happen with active part of security**? Of course we're talking about ethical hacking and penetration testing. The major part of cloud providers doesn't allow to perform hacking tasks in their platform (or very limited), **even if you only attack your own services**!

**IdsFree** allow you to do:

1. **Hacking** tasks **without raise alert into Cloud Provider**.
2. Create a **secure and isolated network** to perform your hacking tests.
3. **Automate** your **hacking tasks** following the concept of previous point.

How it works?
=============

To perform the above tasks, **IdsFree** follow these steps:

1. IdsFree uses a SSH connection a virtual machine in your cloud provider.
2. Once connected, idsFree will **create a private and cyphered network** on this virtual machine using *Docker Swarm*.
3. Get **your application** (and their environment requisites) **as a Docker image** and run it attaching it to the previously created network.
4. **Attach** to the network **hacking tools** as docker containers and launch selected attacks through the cyphered and isolated network.
5. Take the **results** of tools and export them in a usable format: **JSON** or **JUnit** format (very useful for integrating with **Jenkins**).
6. **Clean up** the container and network from the virtual machine.

The next image illustrates how the environment are deployed in the cloud provider:

.. image::  https://github.com/bbva/idsfree/raw/master/doc/source/_static/diagrams/hacking-with-idsfree.png
    :width: 400px
    :alt: IdsFree running

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

Currently, idsFree can launch two type of attacks: net | web, and try to choice the best tools to perform the attacks.

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

Contributors are welcome. You can find a list ot TODO tasks in the `TODO.md <https://github.com/bbva/idsfree/blob/master/TODO.md>`_ at the project file.

All contributors will be added to the `CONTRIBUTORS.md <https://github.com/bbva/idsfree/blob/master/CONTRIBUTORS.md>`_ file.

Thanks in advance if you're planning to contribute to the project! :)

License
=======

This project is distributed under `BSD license <https://github.com/bbva/idsfree/blob/master/LICENSE>`_

