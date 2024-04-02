# TaskAPI
This is the main Flask application that handles the communication with the lambdas tasks creation and listing.

## Globals
- `app`: The flask app instance.
- `lambda_client`:  A boto3 client for AWS Lambda.

## Functions

### `/createtask` [POST]

#### Summary 
This code defines a Flask route called `/createtask` that handles a POST request. It generates a unique ID for the task, retrieves data from the request, and creates a payload for a Lambda function. It then invokes the Lambda function with the payload and returns a response.

#### Example Usage
```python
POST /createtask
{
  "task_name": "Task 1",
  "cron_expression": "0 0 * * *"
}
```

#### Code Analysis
##### Inputs
- `task_name` (string): The name of the task.
- `cron_expression` (string): The cron expression for scheduling the task.
___
##### Flow
1. Generate a unique ID for the task.
2. Retrieve the `task_name` and `cron_expression` from the request data.
3. Create a payload for the Lambda function with the task ID, name, and cron expression.
4. Invoke the `createScheduledTask` Lambda function with the payload.
5. If the Lambda function invocation is successful, return a response with a success message and the task ID.
___
##### Outputs
- Success response (status code 201): 
  ```
  {
    "message": "Task scheduled successfully",
    "task_id": "<generated_task_id>"
  }
  ```
- Error response (status code other than 200):
  ```
  {
    "message": "Error creating task"
  }
___
___


### `/list_tasks` [GET]

#### Summary 
This code defines a Flask route named `list_tasks` that handles a GET request to '/listtask'. It invokes a Lambda function named 'listScheduledTask' using the Boto3 library and retrieves the response. If the response status code is 200, it returns the tasks as a JSON response with a status code of 200. Otherwise, it returns an error message with the corresponding status code.

#### Example Usage
```python
GET /listtask
```

#### Code Analysis
##### Inputs
- None
___
##### Flow
1. The function receives a GET request to '/listtask'.
2. It invokes the 'listScheduledTask' Lambda function using the Boto3 client.
3. The response from the Lambda function is parsed as JSON.
4. If the response status code is 200, the tasks are extracted from the response body.
5. The tasks are returned as a JSON response with a status code of 200. If the response status code is not 200, an error message is returned with the corresponding status code.
___
##### Outputs
- If successful, a JSON response containing the tasks with a status code of 200.
- If unsuccessful, an error message with the corresponding status code.
___
