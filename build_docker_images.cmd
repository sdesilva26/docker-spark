docker build -f Dockerfile_master -t sdesilva26/spark_master -t sdesilva26/spark_master:0.0.1 .
docker build -f Dockerfile_worker -t sdesilva26/spark_worker -t sdesilva26/spark_worker:0.0.1 .
docker build -f Dockerfile_submit -t sdesilva26/spark_submit -t sdesilva26/spark_submit:0.0.1 .

docker push sdesilva26/spark_master
docker push  sdesilva26/spark_master:0.0.1
docker push sdesilva26/spark_worker
docker push sdesilva26/spark_worker:0.0.1
docker push sdesilva26/spark_submit
docker push sdesilva26/spark_submit:0.0.1