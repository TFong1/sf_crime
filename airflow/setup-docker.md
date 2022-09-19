# How to Set Up Apache Airflow Environment

## Create Docker Configuration Files

Create the following files to run Airflow in a Docker container:

* docker-compose.yaml -- modified version of the official [Docker setup file](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml) for the latest Airflow version.

* Dockerfile -- installs any required software to the container when the Docker container is built.  Referenced in docker-compose.yaml.

* .env -- specifies the environment variables for the container instance when it is run.  This file is referenced in docker-compose.yaml.

* requirements.txt -- specifies the python libraries that are installed in the container when the Docker image is built.  Referenced in Dockerfile.

## Build Docker Image

Build the image using the following command:

    docker-compose build

## Initialize Airflow containers (scheduler, database, and other configuration settings)

Run the following command to initialize Airflow:

    docker-compose up airflow-init
