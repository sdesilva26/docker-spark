# Docker-Spark-Tutorial
This repo is intended to be a tutorial walkthrough in how to set up and use a Spark cluster running inside Docker containers. 

I assume some familiarity with Docker and its basic commands such as build and run. Everything else will be explained in this file.

We will build up the complexity to eventually a full architecture of a Spark cluster running inside of Docker containers in a 
sequential fashion so as to hopefully build the understanding. The table of contents below shows 
the different architectures we will work through.

## TABLE OF CONTENTS
* [Create Docker images](#create-docker-images)
    * [Building images from scratch](#building-images-from-scratch)
    * [Pulling images from repository](#pulling-images-from-repository)
* [Docker networking](#docker-networking) 
  * [Containers on single machine](#containers-on-single-machine)
  * [Containers on different machine](#containers-on-different-machine)
  
  
## Create Docker images

#### Building images from scratch
If you wish to build the Docker images from scratch clone this repo.

Next, run the following commands
```
docker build -f Dockerfile_base -t {YOUR_TAG} .
docker build -f Dockerfile_master -t {YOUR_TAG} .
docker build -f Dockerfile_worker -t {YOUR_TAG} .
```
and then you may wish to push these images to your repository on Docker or somewhere else 
using the 'Docker push' command.

#### Pulling images from repository
Alternatively, you can pull the pre-built images from my repository. Simply run
the following commands
```
docker pull sdesilva26/spark_master:latest
docker pull sdesilva26/spark_worker:latest
```
*NOTE: You do not need to pull sdesilva26/spark_base:0.0.1 because, as the name suggests,
this image is used as a base image for the other two images and so is not needed on your machine.*

## Docker networking

Now let's see how to get the containers communicating with each other. First
we shall show how to do when the containers are running on the same machine and
then on different machines.

### Containers on a single machine

Most of the following is taken from Docker's website in their section 
about [networking with standalone containers](#https://docs.docker.com/network/network-tutorial-standalone/).

Docker running on your machine under the hood starts a Docker daemon which interacts
with tthe linux OS to execute your commands.(*NOTE: if you're running Docker on a 
non-linux host, docker actually runs a VM with a linux OS and then runs the Docker
daemon on top of the VM's OS.*)

By default, when you ask the Docker daemon to run a container, it adds it to the
default bridge network called 'bridge'. You can also define a bridge network yourself.

We will do both. First let's use the default bridge network. Let's also run a container
with the image for the Spark master and also one for the Spark worker. Our architecture therefore
looks like the figure below. 

### Containers on different machines

