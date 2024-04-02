# Nuwehack Terraform Cloud Tasker

The **Nuwehack Terraform Cloud Tasker** project aims to create a task management system using AWS Lambda functions and a Flask-based API. This system allows users to schedule and manage tasks efficiently. Below, you'll find instructions for setting up the project.

## Project Structure

The project is organized into the following directories:

```
nuwehack-terraform-cloud-tasker/
├── Infraestructure
│   ├── lambda
│   │   ├── create_scheduled_task.py
│   │   ├── list_scheduled_task.py
│   │   ├── execute_scheduled_task.py
│   │   ├── lambda_1.zip
│   │   ├── lambda_2.zip
│   │   ├── lambda_3.zip
│   │   └── README.md
│   └── Terraform
│       ├── main.tf
│       └── policy.json
├── taskapi
│   ├── app.py
│   └── README.md
├── README.md
├── .gitignore
└── requirements.txt
```

- **`Infraestructure`**: Contains the infrastructure-related code and configuration.
  - **`lambda`**: This directory holds the AWS Lambda functions. You can find the Lambda functions (`create_scheduled_task.py`, `list_scheduled_task.py` and `execute_scheduled_task.py`) here.
      - **`create_scheduled_task.py`**: This is the 1st Lambda that creates the task in the DynamoDB table `Tasks`.
      - **`list_scheduled_task.py`**: This is the 2nd Lambda that get a list of tasks that are in the DynamoDB table `Tasks`.
      - **`execute_scheduled_task.py`**: This is the 3rd Lambda that creates an item in an S3 bucket called `taskstorage`.
      - **`lambda_1.zip`**: This zip contains a file called `lambda_function.py` that contains the code of the 1st Lambda `createScheduledTask`.
      - **`lambda_2.zip`**: This zip contains a file called `lambda_function.py` that contains the code of the 2nd Lambda `listScheduledTask`.
      - **`lambda_3.zip`**: This zip contains a file called `lambda_function.py` that contains the code of the 3rd Lambda `executeScheduledTask`.
      - **`README.md`**: Provides additional details about the Lambdas and its Usage.
  - **`Terraform`**: The Terraform configuration for creating the necessary AWS resources. Key files include `main.tf` (defining resources) and `policy.json` (IAM policy for Lambda functions).

- **`taskapi`**: Contains the Flask-based API for managing lambda tasks.
  - **`app.py`**: The main Flask application that handles lambda task creation and listing.
  - **`README.md`**: Provides additional details about the API setup and endpoints.

## Installation Steps

Follow these steps to set up the project:

1. **Install Requirements**:
   - Navigate to the root folder of your project.
   - Install the required Python packages:
     ```
     pip install -r requirements.txt
     ```

2. **Lambdas Setup**:
   - Change directory to `Infraestructure/Terraform`:
     ```
     cd Infraestructure/Terraform
     ```
   - Initialize Terraform:
     ```
     terraform init
     ```
   - Plan the infrastructure changes:
     ```
     terraform plan
     ```
   - Apply the changes:
     ```
     terraform apply
     ```


3. **TaskAPI Setup**:
   - Change directory to `taskapi`:
     ```
     cd ../taskapi
     ```
   - Run the Flask server  in debug mode (default port is 5000):
     ```
     flask run
     ```

    And  you're ready to go!

## Testing Lambda Functions

1. **Create a scheduled task:**

    ```
    awslocal lambda invoke --function-name createScheduledTask --payload '{"task_name": "my task", "cron_expression": "*/5 * * * *"}' output.json
    ```
2. **List scheduled tasks**:

    ```
    awslocal lambda invoke --function-name listScheduledTask output.json
    ```

3. **Execute a scheduled task:**

    ```
    awslocal lambda invoke --function-name executeScheduledTask output.json
    ```

## Testing TaskAPI Endpoints

1. **Create a task:**

    ```
    curl --location 'http://127.0.0.1:5000/createtask' \
    --header 'Content-Type: application/json' \
    --data '{
        "task_name": "my task name",
        "cron_expression": "*/5 * * * *"
    }'
    ```

2. **List tasks:**

    ```
    curl --location 'http://127.0.0.1:5000/listtask'
    ```


---
### Contributors ###
This project was developed by [Greiberth Pérez](https://github.com/gperezz11) and some cups of coffee😁