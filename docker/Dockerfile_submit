FROM sdesilva26/spark_base

# Set default environment variables. These can also be set at the command line when invoking /bin/spark-submit
ENV MASTER_CONTAINER_NAME=spark-master
ENV SPARK_EXECUTOR_MEMORY=6G
ENV SPARK_EXECUTOR_CORES=3

# Install libraries
COPY ./resources/requirements.txt .
RUN pip install -r requirements.txt

# Copy examples python files into container
COPY ./examples/ /home/examples/
COPY ./resources/log4j.properties ./resources/spark-defaults.conf $SPARK_HOME/conf/

EXPOSE 4040 8888

WORKDIR /home/