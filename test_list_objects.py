

def test_list_objects(client, setup_bucket):
    bucket_name = 'petr_test_bucket'
    get_specific_object = client.get_object(Bucket=bucket_name, Key='file_for_further_uploading.txt')['ResponseMetadata']['HTTPStatusCode']

    assert get_specific_object == 200
    assert len(client.list_objects(Bucket=bucket_name)['Contents']) == 1000