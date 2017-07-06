---
permalink: /quickstart/
title: QuickStart  
title_icon: fa fa-clock-o
body_color: purple
description: 5 minutes start tutorial about idsFree and basic concepts
intro: true
---

What's idsFree?
===============

*idsFree* is a project that allows to create and run some hacking-related tasks in public cloud provides (AWS, GAE, Digital Ocean...). 

The project was born to aims to permit test **your own** applications inside a public infrastructure, **NOT for launch hacking attack to outside using cloud providers as attacks launchers**.


A quick use case
================

Imagine that you have a just developer application. 


My applications should 


Install idsFree
===============

{% highlight ruby %}
> python3.5 -m pip install idsfree
{% endhighlight %}

Prepare remote environment
==========================

**IdsFree** checks if a remote system has all the necessary conditions to run. An examples of usage are:

**Check remote system by passing the password in command line**

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -P MY_PASSWORD prepare
[ * ] Starting preparation of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Initialization Swarm at IP: 192.168.111.129
[ * ] Creating new encrypted network: DgJXoXmeYhASHjmSV
{% endhighlight %}

**Check remote system and tell to idsFree ask for the password**

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -A prepare
[ * ] Starting preparation of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Initialization Swarm at IP: 192.168.111.129
[ * ] Creating new encrypted network: DgJXoXmeYhASHjmSV
{% endhighlight %}

Launch automatic attacks
========================

*idsFree* could performs attack for *net* and *web* environments and can report in *JSON* and *JUnit* compatible format. 
 
If you wan to launch attack and report in **JUnit**:

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -P MY_PASSWORD run_attacks  -p  6379 -t net -s redis redis -o results.xml -e junit
[ * ] Starting attacks of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Generating results as 'JUnit' format, in file: 'results.xml'
{% endhighlight %}

If you wan to launch attack and report in **JSON** and ask for the remote password:

{% highlight ruby %}
> idsfree -v -H 192.168.111.129  -d -U root -A run_attacks  -p  6379 -t  net -s redis redis -o results.json -e json
[ * ] Starting attacks of remote host...
[ * ] Checking remote machine for minimum requisites
[ * ] Creating temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Removing temporal encrypted network: lEvXBfPNVmoCZyFmKJsnPSADJjrUoxmxjFst
[ * ] Generating results as 'json' format, in file: 'results.json'
{% endhighlight %}
    
For more information about the options and configurations for automatic attacks, check 