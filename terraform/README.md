# How to Set Up Terraform Environment

## Flow

1. Create main.tf file.
2. Create Optional variables.tf file.
3. Refresh Google service account's auth token for this session.

        gcloud auth application-default login

4. Initialize state file (.tfstate)

        terraform init

5. Check for changes to new infrastructure plan

        terraform plan -var="project=<your-gcp-project-id>"

6. Create new infrastructure

        terraform apply -var="project=<your-gcp-project-id>"

## Optional

Delete infrastructure after you complete your work to avoid costs on any running services

    terraform destroy

