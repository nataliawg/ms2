import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def check_aws_credentials():
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C://Users//NATALIA WATSON//OneDrive//Documentos//cloud computing//proyecto2//Backend-Utec-GO//microservicio 2//.aws//credentials"
    try:
        session = boto3.Session()

        sts = session.client('sts')
        credentials = session.get_credentials()
        identity = sts.get_caller_identity()
        print("Las credenciales de AWS son válidas.")
        print(f"Cuenta: {identity['Account']}, ARN: {identity['Arn']}")

    except NoCredentialsError:
        print("No se encontraron credenciales de AWS o las credenciales son inválidas.")
    except ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            print("Acceso denegado. Verifica tus permisos.")
        else:
            print(f"Ocurrió un error inesperado: {error}")

check_aws_credentials()