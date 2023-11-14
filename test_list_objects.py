

def test_list_objects(client, setup_bucket):
    bucket_name = 'petr_test_bucket'

    # With these two files I check that after 1000 objects additional ones are not missing after adding
    client.upload_file('data/file_for_further_uploading.txt', bucket_name, 'file_for_further_uploading.txt')
    # Adding another type of file for a change
    client.upload_file('data/pytest_logo_curves.svg', bucket_name, 'pytest_logo_curves.svg')

    get_specific_object = client.get_object(Bucket=bucket_name, Key='file_for_further_uploading.txt')['ResponseMetadata']['HTTPStatusCode']
    get_specific_object_image = client.get_object(Bucket=bucket_name, Key='pytest_logo_curves.svg')['ResponseMetadata']['HTTPStatusCode']


    assert get_specific_object == 200
    assert get_specific_object_image == 200
    assert len(client.list_objects(Bucket=bucket_name)['Contents']) == 1000