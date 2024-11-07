import json
import boto3

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')

def crear_empleo(event, context):
    try:
        token = event['headers']['Authorization']
        payload = json.dumps({'token': token})
        lambda_client.invoke(
            FunctionName='ValidarTokenAcceso',
            InvocationType='RequestResponse',
            Payload=payload
        )

        body = json.loads(event['body'])
        tenant_id = body['tenant_id']
        empleo_id = body['empleo_id']
        empleo_datos = body['empleo_datos']

        table = dynamodb.Table('t_empleo')
        table.put_item(Item={
            'tenant_id': tenant_id,
            'empleo_id': empleo_id,
            **empleo_datos
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Empleo creado exitosamente"})
        }
    except Exception as error:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': str(error)})
        }
