# Apache Spark

## Introduction
Here I am going to try to explain firstly the main terms you will hear when using Apache Spark
and then move on to how to tune a spark cluster for optimal performance.

## Apache Spark Terms & Architecture
To understand how to tune a Spark cluster for optimal performance the terms and structure of a
cluster need to be define and understood.

### Architecture
The basic architecture of an Apache Spark cluster is as follows

![Alt text](images/cluster-overview.png)

The three main nodes in a Spark cluster are the driver node, master node and the worker nodes
. The driver node holds the main() method and the spark context. In the spark context the user
defines how much of the cluster resources they wish to use for the program in the driver node
. From the driver node a user would submit their program to the cluster. 

The first step after submitting a program to the cluster is to communicate how much
resources the driver wants to the cluster manager (what I call the master node). The cluster
manager is the gate keeper of the cluster
. It knows how much resources the cluster has available at any moment in time as well as
which worker nodes are busy and which are free.

Next, the cluster manager then needs to acquire the requested resources from the worker nodes.

Then the cluster manager delegates the work to be carried out to the worker
nodes. The driver program then sends the program's code to the worker nodes that have been
assigned to do the work required. The worker nodes carry out the required work and
communicate the results directly back to the driver node. The cluster manager is responsible for
making sure the program is completed. For instance, if a worker node fails, it is the cluster
manager's responsibility to deletegate that worker node's work to another node.

That is the course-grained explanation of a Spark cluster's physical architecture. I will now go
on to explain what happens when you execute a program in a Spark cluster.

### Execution 
A user in spark specifies a series of transformations followed by an action. Once an action is
called in Spark an execution plan is built up behind the scenes. This is the series of steps
that each worker node needs to carry out on its piece of the data to return the result defined
by the action. This execution plan is called a **job**. 

Because of Spark's lazy evaluation, before the cluster executes the job Spark breaks the job down into **stages**. For example
, a single job could be broken down into 3 stages for example. Stage boundaries are defined by a
 point in the execution plan where the cluster would have to shuffle or move data around the
  cluster. I.e. the worker nodes now need data from other worker nodes. Common examples of a
   stage boundary is when a groupByKey() transformation is encountered in the execution plan.
   
Now that we know a stage is a set of work that a worker node can compute independently of the
other worker nodes we can break a stage down even further. A single stage gets broken down into
**tasks**. A task is a unit of work that can be computed in parallel on a single worker node. For
 example, if a worker node has 4 cores then the task can be run in parallel on these 4 cores. A
task boundary is defined as when a subsequent transformation needs the result of the previous
transformation to carry out its task. For example, reading in a text file and then splitting
 lines into key value pairs would be two tasks. The key value mapping transformation cannot
take place until the file has been read in to the worker nodes.  

All of this can be summarised into the diagram below. The diagram shows the directed acyclic
graph (DAG) for an example job. The DAG is what is created by Spark when you submit an
application and then this is converted by Spark to actually get a physical execution plan. You
can see that this single job is split into 3 stages. These stages are defined by the exchange
transformation because this operation requires data to be shuffled (exchanged) around the
cluster. Each stage is split into multiple tasks. Each tasks can be run in parallel on as
many cores as the user wishes.

![Alt text](images/job_stage_task_layout.png)

A further subtly comes from the fact that within a worker node there is usually multiple
**executors**. Worker nodes are just machines or computers that attached to the Spark cluster. The
name is a bit misleading as it is the executors that actually do the work. The driver node
specifies when it submits an application how many cores each executor
should each have access to, and how much memory they should each have access to.

This is easiest to understand with an example. Let's say that the driver program submits an
application and asks for each executor to have 4 cores and each executor to have 5GB of RAM
. Lets also imagine that each worker node in the cluster is a machine in the cloud with 23 cores
and 32 GB of RAM on each machine. Spark will now try to create as many executors as possible on
each worker node. For this case I just described, where an executor should have 4 cores and
5GB of memory each worker node will create 4 executors. Thus of the 23 cores and 32GB of
memory on each worker node, 16 cores and 20GB of memory will be taken by the 4 executors
. See the image below. Therefore, there will be 3 cores and 12 GB of memory left over.
  
 ![Alt text](images/example_worker_with_executors.png)

Now we submit a job to the cluster. If we concentrate on this worker node for now. Stage 0 is
 loaded and the DAG given for that stage which consists of 3 tasks. Now the 4 executors on this
  node start executing this tasks in parallel on all of the cores available to them. So you have
   16 cores running the same task with a different chunk of the data. This first task might be
    loading the data.
 
 ![Alt text](images/example_worker_with_executors_stage0_task1.png)

Once task 1 is finished the executor cores move on to task 2. At this point all the tasks are
 able to be run without any of the worker nodes, or executors having to communicate with each
  other. Let's imagine this second tasks is some map function that splits text up into words and
   make key value pairs such that (key: word, value: 1). So we create a dictionary where each
    word is the key and its value is 1 to show it has appeared in the text.

![Alt text](images/example_worker_with_executors_stage0_task2.png)

Now we define the next transformation which is a reduceByKey(). Because each of the workers have
 different chunks of data, to reduce by key the executors must communicate to shuffle their data
  aorund such that all key's for the word "hello" end up on one executor and then they can be
   reduced.
   
![Alt text](images/example_worker_with_executors_stage0_task3.png)

What happens is, first the executors perform a reduceByKey() locally on their chunk of data. And
 then all the workers nodes communicate to pass around key's. After the reshuffle a chunk of data
  contains all occurances of a particularly key. For example, after the shuffle all keys
   = "something" will be on one executor. Since the cluster had to shuffle data around we have
    defined a stage boundary, the final part of this reduce is now the start of a new stage.
    
![Alt text](images/example_worker_with_executors_stage1_task1.png)

This is how a Spark cluster divides up your program's job to execute in parallel.

### Terms
Here I put formal definitions of all the Spark specific terms I introduced in the previous section. 

*NOTE: Some of these terms are terms that I use, I will denote these with a **.

| Term        | Definition           | Alias'  |
| ------------- |:-------------:| -----:|
| Driver node      | The machine where the main() method of your program resides | driver program, spark-submit node |
| Master node*      | The machine that runs your cluster manager (Standalone, YARN, Mesos)      |    |
| Worker node | A machine that's resources are available for use in a Spark application      |    |
| Cluster Manager | An external service for acquiring resources on the cluster. Is in charge of allocation of work      |    |
| Job | A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action (e.g. save, collect); you'll see this term used in the driver's logs.     |    |
| Stage | Each job gets divided into smaller sets of tasks called stages that depend on each other (similar to the map and reduce stages in MapReduce); you'll see this term used in the driver's logs.   |    |
| Task |  A unit of work that will be sent to one executor. It is carried out in parallel on all the executor's cores  |    |



## Spark Tuning