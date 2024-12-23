# How to Set Up Terraform Environment

This project uses Terraform to provision resources in Google Cloud Platform (GCP).

## Provision GCP Resources

1. Create `main.tf` file
    * This file defines the infrastructure used in this project.
2. Create `variables.tf` file
    * This file contains the values for the variables used in the main.tf file.
3. Refresh Google service account's auth token
    * If you have not created a Google Cloud Platform account and project, do so before executing the commands below. Follow [this link](../gcp/) to set up Google Cloud Platform.
    * Execute the following command:

        ```sh
        gcloud auth application-default login
        ```

4. Initialize state file (`.tfstate`)

    ```sh
    terraform init
    ```

5. Check for changes to new infrastructure plan

    ```sh
    terraform plan -var="project=your-gcp-project-id"
    ```

    * Replace "your-gcp-project-id" with your actual Google Cloud Plaform Project ID.

6. Create new infrastructure

    ```sh
    terraform apply -var="project=your-gcp-project-id"
    ```

    * Replace "your-gcp-project-id" with your actual Google Cloud Plaform Project ID.

## Delete Infrastructure (*Optional*)

Delete infrastructure after you complete your work to avoid costs on any running services. Run this command to delete Google Cloud Platform resources:

```sh
terraform destroy
```

Now the infrastructure is ready to be used by [Airflow](../airflow/).
