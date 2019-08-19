import boto3
import uuid
import logging
from botocore.exceptions import ClientError

def listmybuckets():
	s3=boto3.resource('s3')
	for bucket in s3.buckets.all():
		print(bucket.name)


def create_bucket(bucket_name, region=None):
	try:
		if region is None:
			s3_client = boto3.client('s3')
			s3_client.create_bucket(Bucket=bucket_name)
		else:
			s3_client = boto3.client('s3', region_name = region)
			location = {'LocationConstraint': region}
			s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
	except ClientError as e:
		logging.error(e)
		return False
	return True

def upload_file(file_name, bucket, object_name=None):

	if object_name is None:
		object_name = file_name

	s3_client = boto3.client('s3')

	try:
		response = s3_client.upload_file(file_name, bucket, object_name)
	except ClientError as e:
		logging.error(e)
		return
	return True

def transfer_file(source_bucket,source_file, target_bucket):
	s3 = boto3.resource('s3')
	copy_source = {
		"Bucket": source_bucket,
		"Key": source_file
		}
	bucket = s3.Bucket(target_bucket)
	bucket.copy(copy_source, source_file)

#transfer_file("uniikkiamparibardhul", "index.html", "asdasdadasdasdafegwsgsrhwrhaerhaerhaerhaerh")

def create_presigned_url(bucket_name, object_name, expiration=3600):


    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def listMyiisiituus():
	ec2client = boto3.client('ec2')
	response = ec2client.describe_instances()
	for reservation in response["Reservations"]:
		for instance in reservation["Instances"]:
			print(instance)
			print(instance["InstanceId"])


	listMyiisiituus()

