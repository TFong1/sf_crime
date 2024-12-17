# San Francisco Crime Data Engineering Capstone Project

This document provides an overview of how the project is constructed and steps I took to create the project.

## Project Architecture

Below is a pictoral description of the architecture used in this project.

![San Francisco Crime Data Project Architecture](./images/SF-crime-architecture.png)

To summarize, the Airflow DAG will extract the data from the San Francisco data portal via Socrata Open Data API and upload parquet files to the data lake. From there data is moved from the lake to warehouse. dbt will transform the data in the warehouse to be used by Google Looker Studio.

## Steps to Create Project

This document outlines the steps to recreate this project.

1. [Set Up Google Cloud Platform Project](./gcp/)
2. [Create Infrastructure Using Terraform](./terraform/)
3. [Set Up Data Pipeline Using Airflow](./airflow/)
4. [Load Data Lake Files to Staging Area](./SQL/)
5. [Transform Data Using dbt](./dbt/)

## Components

Below are some of the links to the components used to create this project.

* [Google Cloud Platform](https://cloud.google.com)
* [Terraform](https://www.terraform.io)
* [Apache Airflow](https://airflow.apache.org)
* [dbt](https://getdbt.com)
* [Socrata Open Data Application Programming Interface (SODA)](https://dev.socrata.com/)
* [Google Looker Studio (Formally Google Data Studio)](https://lookerstudio.google.com)
