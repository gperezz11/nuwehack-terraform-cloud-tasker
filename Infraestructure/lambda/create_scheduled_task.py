import json
import boto3
import uuid
import os

# Inicializa el cliente de DynamoDB
dynamodb_endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Tasks')

def create_scheduled_task(event, context):

    # Genera un ID único para la tarea
    task_id = str(uuid.uuid4())

    # Obtiene los datos del evento
    try:
        task_name = event['task_name']
        cron_expression = event['cron_expression']
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Invalid input data: {e}'})
        }

    # Validar datos del input
    if not task_name or not cron_expression:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid input data'})
        }

    # Crea el ítem para insertar en DynamoDB
    item = {
        'task_id': task_id,
        'task_name': task_name,
        'cron_expression': cron_expression
    }
    try:
        # Inserta el ítem en la tabla DynamoDB
        table.put_item(Item=item)

        # Devuelve una respuesta
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task created successfully', 'task_id': task_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error creating task: {e}'})
        }