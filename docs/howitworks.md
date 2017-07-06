---
permalink: /howitworks/
title: How idsFree works?  
title_icon: fa fa-cogs
body_color: blue
description: What's under the hoods and how idsFree could does hacking tasks safe
intro: true
---

Forewords
=========

*idsFree* was designed with to ideas in mind:
 
- Automatize some hacking-related task.
- Provide a safe & useful tool for building isolated environments for pentesters that need to perform hacking tasks. 
- Be able to perform these hacking tasks in cloud provided securely and without affect other cloud clients.

The above tasks could be done without raise any alerts into could provider.

Building the environment
========================

Independently of the purpose that you was run *idsFree* it will follow these common steps: 

1. IdsFree uses a SSH connection to a virtual machine in your cloud provider.
2. Once connected, idsFree will **create a private and cyphered network** on this virtual machine using *Docker Swarm*.
3. Then get **your application** (and their environment requisites), **packaged as a Docker image**, and attach it to the just created network.
4. Then **Attach** to the network the **hacking tools**, as a docker containers.

Automatized hacking
-------------------

Starting at point 4 of previous common steps, to perform automatized tasks, *idsFree* does:

5. Launch selected attacks through the cyphered and isolated network
6. Take the **results** of tools and export them in a usable format: **JSON** or **JUnit** format (very useful for integrating with **Jenkins**).
7. **Clean up** the container and network from the virtual machine.

Build a lab for pentesters
--------------------------

Starting at point 4 of previous common steps, to perform automatized tasks, *idsFree* does: 

5. Attach a Kali Linux, as a Docker container.
6. Open an SSH port from outside throught this container.
7. Provide to the auditor the SSH connection parameters. 

At this point, when *idsFree* finishes the process, the pentester (auditor) will be able to connect from their machine to the just created environment, pointing to the *Kali Linux* machine.

The next image illustrates the resulting environment visually:

![idsFree](/assets/images/hacking-with-idsfree.png)


Sharing information
---------------------

*idsFree* uses GlusterFS to create a cluster of data. 


Useful links:

- [Using GlusterFS with Docker swarm cluster](http://embaby.com/blog/using-glusterfs-docker-swarm-cluster/)
- [How to Use Docker Machine to Create a Swarm Cluster](https://www.linux.com/learn/how-use-docker-machine-create-swarm-cluster)
- [Adding an existing docker host to docker machine : a few tips](https://blog.dahanne.net/2015/10/07/adding-an-existing-docker-host-to-docker-machine-a-few-tips/)
- [Swarm Machines or Having fun with Docker Machine and the new Docker Swarm orchestration](https://blog.hypriot.com/post/swarm-machines-or-having-fun-with-docker-machine-and-the-new-docker-swarm-orchestration/)


Application with service dependencies
=====================================

docker compose info