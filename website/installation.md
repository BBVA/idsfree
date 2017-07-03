---
permalink: /install-config/
title: Installation & configuration
title_icon: fa fa-book
body_color: green
description: How to install and configure idsFree and the required environment and machines 
intro: true
---

Install idsFree package
=======================

Install idsFree is very simple, depending of the release you want, you can install:

- stable version (**recomended**).
- development version.

Stable version
--------------

{% highlight ruby %}
> python3.5 -m pip install idsfree
{% endhighlight %}


Development version
-------------------

{% highlight ruby %}
> python3.5 -m pip install idsfree
{% endhighlight %}



Provisioning new Machines for *idsFree*
=======================================






Running complex architectures
=============================

Many times your applications must have many dependecies

Configuration
=============

File based configuration
------------------------

*idsFree* could be configured using global file config.
 
This file should be placed in one of three places:

- Your home.
- Current directory.

The file should have the name **.idsfreerc** and should have this structure:

{% highlight ruby %}
[DEFAULT]
timeout = 10
remote_host = 127.0.0.1
remote_port = 22
remote_user = ubuntu
remote_password = MYPASSWORD
cert_path = ~/.ssh/my_custom_pem.pem
{% endhighlight %}

The working mode is very simple: their parameter missing when *idsFree* will be called will be taken from config file.

Remote access using certificate
-------------------------------

Using certificates is useful than password access to the remote systems. *idsFree* allow to use *PEM* certificates. To do that should use the certificate option:

- In command line, using *--cert-path* option.
- In config file, using *cert_path* value.

{% highlight ruby %}
> idsfree --cert-path /home/me/.ssh/my_cert.pem -d -v run_attacks -redis -o results.xml
{% endhighlight %}

Or, if you are using config file:

{% highlight ruby %}
[DEFAULT]
cert_path = /home/me/.ssh/my_cert.pem
{% endhighlight %}

And then run:

{% highlight ruby %}
> idsfree -d -v run_attacks -redis -o results.xml
{% endhighlight %}