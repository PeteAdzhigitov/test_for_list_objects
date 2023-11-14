import boto3
import pytest
from botocore.exceptions import ClientError

@pytest.fixture
def client():
    session = boto3.Session()
    s3client = session.client('s3', endpoint_url='https://hb.vkcs.cloud')
    yield s3client

    teardown(client=s3client, bucket_name='petr_test_bucket')

@pytest.fixture
def setup_bucket(client, bucket_name='petr_test_bucket'):
    client.create_bucket(ACL='public-read', Bucket=bucket_name,
                         CreateBucketConfiguration={'LocationConstraint': 'ru-msk'})

    try:
        assert client.head_bucket(Bucket=bucket_name)['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        return 'Bucket hasn\'t been found'

    for number in range(0,1000):
        client.put_object(Body='Some_text_added_to_files', Bucket=bucket_name, Key=f'test_file{number}.txt')

def teardown(client, bucket_name):

    condition = False
    while condition != True:
        objects_to_delete = []
        for key in client.list_objects(Bucket=bucket_name)['Contents']:
            object = {'Key':key['Key']}
            objects_to_delete.append(object)

        client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
        try:
            objects = len(client.list_objects(Bucket=bucket_name)['Contents'])
            if objects != 0:
                continue
        except KeyError:
            condition = True

    delete_bucket = client.delete_bucket(Bucket=bucket_name)
    try:
        assert delete_bucket['ResponseMetadata']['HTTPStatusCode'] == 204
    except ClientError:
        return 'The bucket you tried to delete is not empty'