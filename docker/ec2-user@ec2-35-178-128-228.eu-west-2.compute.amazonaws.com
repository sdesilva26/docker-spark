version: "3"
services:
  spark-master:
    image: "sdesilva26/spark_master:0.0.2"
    ports:
      - "8080:8080"
    networks:
      - spark-net
    deploy:
      placement:
        # set node labels using docker node update --label-add key=value <NODE ID> from swarm manager
        constraints:
          - node.labels.role==master
  spark-worker:
    image: "sdesilva26/spark_worker:0.0.2"
    ports:
      - "8081:8081"
    environment:
      - CORES=3
      - MEMORY=15G
    deploy:
      placement:
        # set node labels using docker node update --label-add key=value <NODE ID> from swarm manager
        constraints:
          - node.labels.role==worker
        replicas: 3
    networks:
      - spark-net
networks:
  spark-net:
    driver: overlay