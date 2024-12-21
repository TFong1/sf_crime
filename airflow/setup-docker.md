# How to Set Up Apache Airflow Environment

Create the Airflow environment by:

1. Create Docker configuration files
2. Build Docker image
3. Initialize Airflow containers

## Create Docker Configuration Files

Create the following files to run Airflow in a Docker container:

* docker-compose.yaml
  * Modified version of the official [Docker setup file](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml) for this project

* Dockerfile
  * Installs required software to the container when the Docker container is built
  * Referenced in docker-compose.yaml

* .env
  * Specifies the environment variables for the container instance when it is run
  * Referenced in docker-compose.yaml

* requirements.txt
  * Specifies the Python libraries to be installed in the container when the Docker image is built
  * Referenced in Dockerfile

## Build Docker Image

Build the Docker image using the following command:

```sh
docker-compose build
```

## Initialize Airflow containers

Run the following command to initialize Airflow:

```sh
docker-compose up airflow-init
```

This command will set up the Airflow scheduler, database, and other configuration settings in the docker-compose.yaml file.

Go back to the [Airflow setup](./README.md#run-all-airflow-services-in-docker) to complete the configuration of Airflow.
