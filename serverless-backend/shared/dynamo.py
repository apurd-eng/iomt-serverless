import boto3
from typing import Any, Dict


def get_item(table_name: str, key: Dict[str, Any]) -> Dict[str, Any] | None:
    table = boto3.resource('dynamodb').Table(table_name)
    resp = table.get_item(Key=key)
    return resp.get('Item')


def put_item(table_name: str, item: Dict[str, Any]) -> None:
    table = boto3.resource('dynamodb').Table(table_name)
    table.put_item(Item=item)
