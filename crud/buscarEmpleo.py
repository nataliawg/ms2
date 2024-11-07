import json
import boto3

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')

def buscar_empleo(event, context):
    token = event.get('headers', {}).get('Authorization')
    if not token:
        return {
            'statusCode': 403,
            'body': json.dumps('Forbidden - No token provided')
        }

    payload = json.dumps({'token': token})
    try:
        response = lambda_client.invoke(
            FunctionName='ValidarTokenAcceso',
            InvocationType='RequestResponse',
            Payload=payload
        )
        result = json.loads(response['Payload'].read())

        if result['statusCode'] != 200:
            return {
                'statusCode': 403,
                'body': json.dumps('Forbidden - Invalid token')
            }

        tenant_id = event['queryStringParameters']['tenant_id']
        empleo_id = event['queryStringParameters']['empleo_id']
        table = dynamodb.Table('t_empleo')
        response = table.get_item(Key={'tenant_id': tenant_id, 'empleo_id': empleo_id})

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Empleo no encontrado')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    except Exception as error:
        print(error)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
