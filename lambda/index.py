import boto3
import json
import string
import os
import logging
import psycopg2
from psycopg2 import errors


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
        # Create database
        create_database_flag = os.environ['CREATE_DATABASE']
        if create_database_flag == "true":
            create_database(master_username, master_password, rds_host, rds_port, "postgres")

        # Connect to newly created database
        conn = psycopg2.connect(user=master_username, password=master_password,
                                host=rds_host, port=rds_port, dbname=database_name)
        conn.autocommit = True
        cursor = conn.cursor()

        # Create user
        usernames = get_pg_usernames(cursor)
        if username in usernames:
            print("User already exists - skipping creation of user")
        else:
            sql = "CREATE USER {} WITH PASSWORD '{}';".format(username, password)
            cursor.execute(sql)

        # Grant privileges
        grant_sql = "GRANT CONNECT ON DATABASE {} TO {};".format(database_name, username)
        grant_sql += "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {};".format(username)
        grant_sql += "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {};".format(username)
        grant_sql += "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO {};".format(username)

        cursor.execute(grant_sql)

        # Close communication with the database
        cursor.close()
        conn.close()
    except Exception as e:
        print('Error while performing provisioning: ', str(e))
        raise e
# end def

def get_pg_usernames(cursor):
    query = "SELECT u.usename AS username FROM pg_catalog.pg_user u;"
    rows = []
    cursor.execute(query)
    for row in cursor:
        rows.append(row[0])
    return rows

def create_database(master_username, master_password, rds_host, rds_port, database_name):
    conn = psycopg2.connect(user=master_username, password=master_password,
                                host=rds_host, port=rds_port, dbname=database_name)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create database
    create_database_flag = os.environ['CREATE_DATABASE']
    if create_database_flag == "true":
        try:
            sql = "CREATE DATABASE {};".format(database_name)
            cursor.execute(sql)
        except errors.DuplicateDatabase as e:
            print('Database already exists')
            pass

    cursor.close()
    conn.close()
    
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
