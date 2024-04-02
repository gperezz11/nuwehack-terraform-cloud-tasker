provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true

  endpoints {
    apigateway     = "http://localhost:4566"
    cloudwatch     = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"
    events         = "http://localhost:4566"
    iam            = "http://localhost:4566"
    sts            = "http://localhost:4566"
    s3             = "http://localhost:4566"
  }
}


# Create Table Tasks in DynamoDB 
resource "aws_dynamodb_table" "tasks_table" {
  name           = "Tasks"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "task_id"

  attribute {
    name = "task_id"
    type = "S"
  }
}


# Create bucket S3
resource "aws_s3_bucket" "task_storage" {
  bucket = "taskstorage"
  acl    = "private"
}

# Lambda 1

resource "aws_lambda_function" "create_scheduled_task" {
  function_name    = "createScheduledTask"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../lambda/lambda_1.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/lambda_1.zip")
  handler          = "lambda_function.create_scheduled_task"
}

# Lambda 2

resource "aws_lambda_function" "list_scheduled_task" {
  function_name    = "listScheduledTask"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../lambda/lambda_2.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/lambda_2.zip")
  handler          = "lambda_function.list_scheduled_task"
}

# Lambda 3


resource "aws_lambda_function" "execute_scheduled_task" {
  function_name    = "executeScheduledTask"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../lambda/lambda_3.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/lambda_3.zip")
  handler          = "lambda_function.execute_scheduled_task"
}




# Create rule EventBridge every-minute
resource "aws_cloudwatch_event_rule" "every_minute" {
  name                = "every-minute"
  schedule_expression = "cron(0/1 * * * ? *)"
  is_enabled          = true
}

# Link rule with Lambda executeScheduledTask
resource "aws_cloudwatch_event_target" "execute_scheduled_task_target" {
  rule      = aws_cloudwatch_event_rule.every_minute.name
  target_id = "1"
  arn       = aws_lambda_function.execute_scheduled_task.arn
}


# Lambda execution role with the necessary trust policy
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}

# Inline policy to grant Lambda functions access to the DynamoDB table
resource "aws_iam_policy" "lambda_dynamodb_policy" {
  name   = "lambda-dynamodb-policy"
  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        Effect   = "Allow",
        Resource = aws_dynamodb_table.tasks_table.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_dynamodb_policy.arn
}
