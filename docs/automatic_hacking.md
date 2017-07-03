---
permalink: /automatic-hacking/
title: Automatic hacking
title_icon: fa fa-caret-square-o-right
body_color: None
description: Launch automatized hacking tasks in the cloud for your Continuous integration cycles 
---

Launch automatic attacks
========================

Also, idsFree can report in two formats: **JSON** and **JUnit**.

**Launch attack and report in JUnit**

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -P MY_PASSWORD run_attacks  -p  6379 -t net -s redis redis -o results.xml -e junit
[ * ] Starting attacks of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Generating results as 'JUnit' format, in file: 'results.xml'
{% endhighlight %}

**Launch attack, report in JSON and ask for password**

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -A run_attacks  -p  6379 -t  net -s redis redis -o results.json -e json
[ * ] Starting attacks of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Generating results as 'json' format, in file: 'results.json'
{% endhighlight %}


Attack types
============

Currently, **idsFree** can launch two type of attacks: 

- **net**: Network oriented attacks. 
- **web**: Web oriented attacks.

*idsFree* will choice the best tools to perform each type of attack.

Results format
==============

Currently *idsFree* could report the results in two formats:

- **JUnit** compatible file.
- **JSON** format.