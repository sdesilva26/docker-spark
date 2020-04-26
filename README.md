# Docker-Spark-Tutorial
This repo is intended to be a walkthrough in how to set up a Spark cluster running inside Docker containers. 

I assume some familiarity with Spark and Docker and their basic commands such as build and run. Everything else will be explained in this file.

We will build up the complexity to eventually a full architecture of a Spark cluster running inside of Docker containers in a 
sequential fashion so as to hopefully build the understanding. 

***
## Tutorial
A full walk through on how to create a Spark cluster running on separate machines inside Docker
containers is container within the [TUTORIAL.md](TUTORIAL.md). The file builds up the complexity
in a sequential fashion so as to help the understanding of the user. It starts off by
demonstrating simple docker container networking, moves to setting up a Spark cluster on a
local machine, and then finally combining the two locally and in a distributed fashion.

#### Prerequisites

I assume knowledge of basic Docker commands such as run, build, etc.

You will need to set up multiple machines with a cloud provider such as AWS or Azure.

***
## Apache Spark
The APACHESPARKTUNING.md explains the main terms involved in a Spark cluster such as worker node, master node, executor,
task, job, etc. The second section of this file describes some rough rules to use when setting the
parameters of your cluster to get optimal performance with some demonstrations.
***
## Examples
The examples/ directory contains some example python scripts and jupyter notebooks for demonstrating various aspects of 
of Spark.

## Getting Started

To get started, pull the following three docker images
```
docker pull sdesilva26/spark_master:latest
docker pull sdesilva26/spark_worker:latest
docker pull sdesilva26/spark_submit:latest
```
Create a docker swarm using
``` 
docker swarm init
```
then attach the other machines you wish to be in the cluster to the docker swarm by copying and
pasting the output from the above command.

Create an overlay network by running the following on one of the machines
``` 
docker network create -d overlay --attachable spark-net
```
On the machine you wish to be the master node of the Spark cluster run
``` 
docker run -it --name spark-master --network spark-net -p 8080:8080 sdeislva26/spark_master
:latest
```
On the machines you wish to be workers run
``` 
docker run -it --name spark-worker1 --network spark-net -p 8081:8081 -e MEMORY=6G -e
     CORES=3 sdesilva26/spark_worker:latest
```
substituting the values for CORES and MEMORY to be cores of the machine - 1 and RAM of machine
- 1GB.

Start a driver node by running
``` 
docker run -it --name spark-submit --network spark-net -p 4040:4040 sdesilva26/spark_submit
:latest bash
```

You can now either submit files to spark using 
``` 
$SPARK_HOME/bin/spark-submit [flags] file 
```

or run a pyspark shell
``` 
$SPARK_HOME/bin/pyspark
```
NOTE: by default the sdesilva26/spark_submit and sdesilva26/spark_worker images will try to
 connect to the cluster manager at spark://spark-master:7077 so if you change the name of the
  container running the sdesilva26/spark_master image then you must pass this change as follows

``` 
docker run -it --name spark-submit --network spark-net -p 4040:4040 -e MASTER_CONTAINER_NAME
=<your-master-container-name> sdesilva26/spark_submit
:latest bash
```

for the submit node and

``` 
docker run -it --name spark-worker1 --network spark-net -p 8081:8081 -e MEMORY=6G -e
     CORES=3 -e MASTER_CONTAINER_NAME=<your-master-container-name> sdesilva26/spark_worker:latest
```
for thw worker node.

These instructions allow you to manually set up a Apache Spark cluster running inside docker
 containers located on different machines. For a full walk-through including explanations and
  a docker-compose version of setting up a cluster see the [TUTORIAL.md](TUTORIAL.md)


## Authors

* Shane de Silva

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Marco Villarreal's](https://github.com/mvillarrealb/) docker images for the starting point for my own docker images 