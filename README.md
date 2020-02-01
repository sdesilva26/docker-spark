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
  * [Containers on single machine](#containers-on-a-single-machine)
  * [Containers on different machine](#containers-on-different-machines)
  
  
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

#### Deafult bridge network
We will do both. First let's use the default bridge network. Let's also run a container
with the image for the Spark master and also one for the Spark worker. Our architecture therefore
looks like the figure below. 

![Alt text](/images/docker_single_machine.png "docker_on_single_machine")

Start the two containers up using
```
docker run -dit --name spark-master sdesilva26/spark_master:0.0.1 bash
docker run -dit --name spark-worker sdesilva26/spark_worker:0.0.1 bash
```
The d flag means to run the container dettached, so in the background, the i flag
indicates it should be interactive so that we can type into it, and the t flag specifies 
the container should be started with a TTY so you can see the input and output.

Check that the containers have started using 
```
docker container ls
```
and you should get something similar to

![Alt text](/images/screenshot1.png "screenshot1")

You can see which containers are connected to a network by using
```
docker network inspect bridge
```
and you should see something similar to the following

![Alt text](/images/screenshot2.png "screenshot2")

Attach to the spark-master container using
```
docker attach spark-master
```
You should the prompt to change now to a # which indicates that you are
the root user inside of the container.

Get the network interfaces as they look from within the container using
```
ip addr show
```
The interface with the title starting with 'eth0"' should display that
this interface has the same IP address as what was shown for the spark-master
container in the network inspect command from above.

Check internet connection from within container using
```
ping -c 2 google.com
```
Now ping spark-worker container using its IP address from the network
```
ping -c 2 172.17.0.3
```
If you know ping by container name it will familiarity
```
ping -c 2 spark-worker
```
Now dettach from spark-master whilst leaving it running by holding down
ctl and hitting p and then q.

#### User-defined bridge network

Create the user-defined bridge network
```
docker network create --driver bridge spark-network
```
Then list the networks
```
docker network ls
```
and you should see

![Alt text](/images/screenshot3.png "screenshot3")

and now inspect the network
```
docker network inspect spark-net
```

![Alt text](/images/screenshot4.png "screenshot4")

The IP address of the network's gateway should now be different to the IP address
of the default gateway. It should also show that no containers are attached to it.

Now stop the two running containers, remove them, then create two new containers
that are attached to the new user-defined network.
```
docker kill spark-master spark-worker
docker rm spark-master spark-worker

docker run -dit --name spark-master --network spark-net sdesilva26/spark_master:latest bash
docker run -dit --name spark-worker1 --network spark-net sdesilva26/spark_worker:latest bash
```
*NOTE: you can only connect to a single network when creating a docker container. But you
can attach it to more networks after using the 'docker network connect <NETWORK_NAME> <CONTAINER_NAME>'
command.*

Again make sure the containers are running and inspect the network to make sure they
have successfully attached to the spark-net network.

The advantage of user-defined networks is as before containers can communicate via
IP address in the network, but they can also resolve a container name to its IP
address in the network now (this is called 'automatic service discovery').

Attach to spark-master and ping spark-worker using its IP address and also its
container name.
```
docker container attach spark-master

ping -c 2 172.18.0.3
ping -c 2 spark-worker
```

Dettach from the container using ctl followed by p and then q. 

In the tutorial linked at the start of this section they go through the case of having
a container in a user-defined network AND the bridge network. It can obviously communicate
with the two containers in spark-net for instance. It could also communicate with a 
container inside just the bridge network but it would have to ping it using its IP
address as specified in the bridge network.


### Containers on different machines

For this section most of this will be following the instructions from Docker's
website about using an [overlay network for standalone containers](#https://docs.docker.com/network/network-tutorial-overlay/).

If you have two different machines then the following section can be skipped.

#### Settting up Amazon EC2 instances
Otherwise you will need to setup at least 2 Amazon EC2 instances (or any other cloud computing provider
you are comfortable with).

1. Go to AWS and select EC2. 
2. Go to launch instance and select *'Amazon Linux AMI 2018.03.0 (HVM),
SSD Volume Type'* as the image type.
3. Select t2.micro
4. Set 'Number of instances' to 2 and leave everything else as default
5. Click through to 'Configure Security Group' and select 'Create a new security group'
6. As detailed in Docker's tutorial, 'Each host must have,.... the following ports open
 between the two Docker hosts:

    - TCP port 2377
    - TCP and UDP port 7946
    - UDP port 4789

If you’re using AWS or a similar cloud computing platform, the easiest configuration is
to use a security group that opens all incoming ports between the two hosts and the 
SSH port from your client’s IP address.'
7. Launch the instances and associate a key with your instances.

Now that you have launched your ec2 instance you need to install docker. To do this
type the following
```
sudo yum install docker -y

sudo service docker start

sudo docker run hello-world

```
To avoid having to use sudo all the time follow these [instructions](#https://github.com/sindresorhus/guides/blob/master/docker-without-sudo.md)
and then disconnect from your instance and connect back to it again. You should now
be able to run Docker commands without sudo.

Finally login to your repo and pull the spark_master and spark_worker image, one into each of the
instances.

For example, on instance 1
```
docker pull sdesilva26/spark_master:latest
```

and on instance 2,
```
docker pull sdesilva26/spark_worker:latest
```

You're all set to go!

#### Default overlay network

Now that you have two separate machines running Docker that are on the same network
you have an architecture like this

![Alt text](/images/docker_two_machines1.png "docker_on_two_machines1")

There is two instances running Docker inside of the same subnet
which is itself inside of your personal bit of the Amazon cloud
called a virtual private cloud (VPC).

We want to create a network that encapsulates both Docker containers. To do
this we will first create a Docker swarm, which essentially links the daemons together,
and then we will create an overlay network and put our containers in that network.