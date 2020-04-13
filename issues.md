# Issues & Resolutions
Here I will detail any problems I come across as I try to go through this tutorial.

- Docker Memory Issues (#docker-memory-issue)

 ##Docker Memory Issue
If you are not able to pull/build the spark-submit image and get an error message saying 'no space left on device', it may be that it is too big for your docker setup to handle. The quick fix is to clean everything from Docker using:

`docker system prune`

Otherwise you can check the base image size:

`docker info`

You should get something similar to 
![Alt text](images/docker_info_1 "docker info")

This tells you how big a docker image can be on your current storage driver. You may need to increase this using:

`sudo service docker stop`
`sudo dockerd --storage-opt dm.basesize=20G`
`sudo service docker start`

You're directory that stores all the different layers of docker images is probably full so delete it using the following commands:

`sudo service docker stop`
`rm -r /var/lib/docker/`
`sudo service docker start`

 Try pulling/building image again now.
