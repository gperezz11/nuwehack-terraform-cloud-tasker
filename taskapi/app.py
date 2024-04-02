from flask import Flask, request, jsonify
import boto3
import json
import uuid

app = Flask(__name__)

# Cliente de Lambda
lambda_client = boto3.client('lambda', endpoint_url='http://localhost:4566')

@app.route('/createtask', methods=['POST'])
def create_task():
    # Genera un ID único para la tarea
    task_id = str(uuid.uuid4())

    # Obtiene los datos del request
    data = request.get_json()
    try:
        task_name = data.get('task_name')
        cron_expression = data.get('cron_expression')

    except AttributeError as e:
        return jsonify({'message': f'Invalid request data: {e}'}), 400
    # Crea el payload para la función Lambda
    payload = {
        'task_id': task_id,
        'task_name': task_name,
        'cron_expression': cron_expression
    }

    # Invoca la función Lambda
    response = lambda_client.invoke(
        FunctionName='createScheduledTask',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    if response['StatusCode'] != 200:
        return jsonify({'message': 'Error creating task'}), response['StatusCode']
    # Devuelve una respuesta
    return jsonify({'message': 'Task scheduled successfully', 'task_id': task_id}), 201

@app.route('/listtask', methods=['GET'])
def list_tasks():
    # Invoca la función Lambda
    response = lambda_client.invoke(
        FunctionName='listScheduledTask',
        InvocationType='RequestResponse'
    )

    # Obtiene la respuesta de la función Lambda
    result = json.loads(response['Payload'].read())
    try:
        if result['statusCode'] != 200:
            return jsonify({'message': 'Error listing tasks'}), result['statusCode']
        else:
            tasks = json.loads(result['body'])
            return jsonify(tasks), 200
    except KeyError:
        return jsonify({'message': 'Error listing tasks'}), 500

    # Devuelve la lista de tareas como un objeto JSON

if __name__ == '__main__':
    app.run(debug=True)
