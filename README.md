# Docker-Spark-Tutorial
This repo is intended to be a walkthrough in how to set up a Spark cluster running inside Docker containers. 

I assume some familiarity with Spark and Docker and their basic commands such as build and run. Everything else will be explained in this file.

We will build up the complexity to eventually a full architecture of a Spark cluster running inside of Docker containers in a 
sequential fashion so as to hopefully build the understanding. 

***
## Tutorial
A full walk through on how to create a Spark cluster running on separate machines inside Docker containers is container within the TUTORIAL.md.
The file builds up the complexity in a seuqential fashion so as to help the understanding of the user. It starts off by demonstrating simple docker container
networking, moves to setting up a Spark cluster on a local machine, and then finally combining the two locally and in a distrbuted fashion.

***
## Apache Spark Tuning
The APACHESPARKTUNING.md explains the main terms involved in a Spark cluster such as worker node, master node, executor,
parallelism, etc. The second section of this file describes some rough rules to use when setting the parameters of your 
cluster to get optimal performance with some demonstrations.
***
## Examples
The examples/ directory contains some example python scripts and jupyter notebooks for demonstrating various aspects of 
of Spark.