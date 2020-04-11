docker build -f Dockerfile_master -t sdesilva26/spark_master -t sdesilva26/spark_master:0.0.2 .
docker build -f Dockerfile_worker -t sdesilva26/spark_worker -t sdesilva26/spark_worker:0.0.2 .
docker build -f Dockerfile_submit -t sdesilva26/spark_submit -t sdesilva26/spark_submit:0.0.2 .

docker push sdesilva26/spark_master:latest
docker push  sdesilva26/spark_master:0.0.2
docker push sdesilva26/spark_worker:latest
docker push sdesilva26/spark_worker:0.0.2
docker push sdesilva26/spark_submit:latest
docker push sdesilva26/spark_submit:0.0.2