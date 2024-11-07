import boto3
import json

lambda_client = boto3.client('lambda')

def validar_token(token):
    params = {
        'FunctionName': 'ValidarTokenAcceso',
        'InvocationType': 'RequestResponse',
        'Payload': json.dumps({'token': token})
    }

    response = lambda_client.invoke(**params)

    result = json.loads(response['Payload'].read())

    if result['statusCode'] == 403:
        raise Exception('Forbidden - Acceso No Autorizado')

    return result
