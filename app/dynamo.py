import boto3

TABLE_NAME = "todos"


def _resource():
    return boto3.resource("dynamodb")


def get_table():
    return _resource().Table(TABLE_NAME)
