---
permalink: /faq/
title: F.A.Q  
title_icon: icon_lifesaver
body_color: None
description: Frequent Asked Questions
---

General
=======

<h3 class="question"><i class="fa fa-question-circle"></i> Is idsFree suitable for Malware analysis?</h3>

**NO**. idsFree runs under Docker umbrella and not uses visualization neither bare-metal approach. So, it makes not sense to use it for malware analysis.  

<h3 class="question"><i class="fa fa-question-circle"></i> My applications need to packaged as any specific way?</h3>

**Yes**. *idsFree* only understands about docker images. You need to package your application into a Docker image and tell to *idsFree* what's ports are you exposing in your applications (or what's port do you want to test).

Then, you need to upload your Docker image to an accessible Docker Registry. *idsFree* will download this image.
 
<h3 class="question"><i class="fa fa-question-circle"></i> My application depends of other services, how can I tell to idsFree that?</h3>

We know that is very strange that an application hasn't any dependency (a database, for example). For that, you could specify a Docker Swarm compose with all of your application dependencies.

For more information, see [How it works](/howitworks/) section.

AWS Problems
============

<h3 class="question"><i class="fa fa-question-circle"></i> My cluster machines can't reach each others</h3>

AWS has the concept of VPC. Each VPC defines the allowed port to be opened. By default, the needed port por idsFree (it's really that Swarm uses) need to be opened in the firewall.
    
The port you should open are:

**TCP**

- 2377
- 7946

**UDP**

- 7946
- 4789

You also need to allow *ip protocol 50*. 

More information at [Swam documentation page](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts).

Linux errors
============

<h3 class="question"><i class="fa fa-question-circle"></i> Why Linux raises 'sudo' command not found?</h3>

*idsFree* uses `sudo` command to launch remote commands. Be sure that sudo command is installed in remote system and your user has permissions to execute `docker` command using sudo.

<h3 class="question"><i class="fa fa-question-circle"></i> When idsFree launches can't find attacked app</h3>

*idsFree* uses very new Docker features that need very new Linux kernel. Be sure you have had updated your system to have newest userlan tools and kernel.  

Usually it should be enough to run `sudo apt dist-upgrade` command.

