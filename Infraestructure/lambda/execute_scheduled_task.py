import json
import boto3
from datetime import datetime

# Inicializa el cliente de S3
s3 = boto3.client('s3')


def execute_scheduled_task(event, context):
    # Define el nombre del bucket y el ítem
    bucket_name = 'taskstorage'
    item_name = f"item-{datetime.now().isoformat()}.txt"

    # Obtiene el contenido del ítem del evento, si está presente
    if 'item_content' in event:
        item_content = event['item_content']
    else:
        item_content = 'Contenido predeterminado del ítem.'

    try:
        # Crea el ítem en el bucket S3
        s3.put_object(Bucket=bucket_name, Key=item_name, Body=item_content)

        # Devuelve una respuesta
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item created successfully', 'item_name': item_name})
        }

    except Exception as e:
        # Si ocurre un error, devolver una respuesta con el mensaje de error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
