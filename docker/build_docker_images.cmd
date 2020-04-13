docker build -rm -f Dockerfile_master -t sdesilva26/spark_master -t sdesilva26/spark_master:0.0.2 .
docker build -rm -f Dockerfile_worker -t sdesilva26/spark_worker -t sdesilva26/spark_worker:0.0.2 .
docker build -rm -f Dockerfile_submit -t sdesilva26/spark_submit -t sdesilva26/spark_submit:0.0.2 .
