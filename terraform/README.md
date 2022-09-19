# How to Set Up Terraform Environment

## Steps

1. Create main.tf file.  This file defines the infrastructure used in this project.
2. Create variables.tf file.  This file contains the values for the variables used in the main.tf file.
3. Refresh Google service account's auth token for this session.  If you have not already created a Google Cloud Platform account and project, do so before executing the commands below.

        gcloud auth application-default login

4. Initialize state file (.tfstate)

        terraform init

5. Check for changes to new infrastructure plan

        terraform plan -var="project=your-gcp-project-id"

   Replace the "your-gcp-project-id" with the actual Google Cloud Plaform Project ID.

6. Create new infrastructure

        terraform apply -var="project=your-gcp-project-id"

   Replace the "your-gcp-project-id" with the actual Google Cloud Plaform Project ID.

## Optional

Delete infrastructure after you complete your work to avoid costs on any running services

    terraform destroy

Now the infrastructure is ready to be used by [Airflow](../airflow/).
