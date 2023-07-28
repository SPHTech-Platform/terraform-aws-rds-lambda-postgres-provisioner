import boto3
import json
import random
import string
import os
import psycopg2
import logging


def lambda_handler(event, context):
    secrets = get_secrets(os.environ['DB_USER_SECRET_MANAGER_NAME'])
    secret_json = json.loads(secrets)
    password = secret_json['password']

    master_secrets = get_secrets(os.environ['DB_MASTER_SECRET_MANAGER_NAME'])
    master_secrets_json = json.loads(master_secrets)
    master_username = master_secrets_json['username']
    master_password = master_secrets_json['password']

    # Set new password to database
    provision_db_and_user(master_secrets_json, secret_json)

    # Test database connection
    try:
        test_db_connection(secret_json['username'], password,
                           secret_json['database'], os.environ['RDS_HOST'], os.environ['RDS_PORT'])

    except Exception as e:
        print('Error while performing test db connection: ', str(e))
        raise e

    print("RDS user and database created successfully.")


def get_secrets(secret_manager_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',
                            region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))

    try:
        secret_response = client.get_secret_value(SecretId=secret_manager_name)
    except Exception as e:
        raise e

    secret_json = secret_response['SecretString']
    return secret_json
# end def


def provision_db_and_user(master_secrets_json, secret_json):
    rds_host = os.environ['RDS_HOST']
    rds_port = os.environ['RDS_PORT']

    username = secret_json['username']
    password = secret_json['password']
    database_name = secret_json['database']

    master_username = master_secrets_json['username']
    master_password = master_secrets_json['password']

    try:
        conn = psycopg2.connect(user=master_username, password=master_password,
                                host=rds_host, port=rds_port, database="postgres")
        conn.autocommit = True
        cursor = conn.cursor()

        # Create user
        sql = "CREATE USER {} WITH PASSWORD '{}' CREATEDB;".format(
            username, password)
        cursor.execute(sql)

        # Create database
        query = "CREATE DATABASE {};".format(database_name)
        cursor.execute(query)

        # Close communication with the database
        cursor.close()
        conn.close()
    except Exception as e:
        print('Error performing provisioning: ', str(e))
        raise e
# end def


def test_db_connection(username, password, database_name, rds_host, rds_port):
    '''Test if the database can be connected using the new password'''

    try:
        conn = psycopg2.connect(user=username, password=password,
                                host=rds_host, port=rds_port, database=database_name)
        cursor = conn.cursor()

        sql = "SELECT 1"
        cursor.execute(sql)

        # Close communication with the database
        cursor.close()
        conn.close()
    except Exception as e:
        raise e
# end def
