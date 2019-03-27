import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError

import config


def main():
    """
    Download a file from S3 of the main AWS account
    Assume role on the second AWS account
    Upload file to S3 of the second account

    """
    # Open a session with 1st aws acc
    session = boto3.session.Session(aws_access_key_id=config.key,
                                    aws_secret_access_key=config.secret)
    s3 = session.resource('s3')

    try:
        s3.Bucket(config.bucket1).download_file(config.remote_fn, config.local_fn)
        print('file {} was downloaded as {}'.format(config.remote_fn, config.local_fn))
    except ClientError as e:
        print(e)

    sts_client = session.client('sts')
    # Assume a role for using 2nd acc
    assumed_role_object = sts_client.assume_role(
        RoleArn="arn:aws:iam::{}:role/{}".format(config.account2_id, config.role),
        RoleSessionName="AssumeRoleSession1"
    )
    # get temporary credentials
    credentials = assumed_role_object['Credentials']

    # starting session with temporary credentials
    session = boto3.session.Session(aws_access_key_id=credentials['AccessKeyId'],
                                    aws_secret_access_key=credentials['SecretAccessKey'],
                                    aws_session_token=credentials['SessionToken'], )
    s3 = session.resource('s3')

    try:
        s3.Bucket(config.bucket2).upload_file(config.local_fn, config.remote_fn)
        print('file {} was uploaded as {} '.format(config.local_fn, config.remote_fn))
    except ClientError as e:
        print(e)
    except S3UploadFailedError as e:
        print(e)


if __name__ == '__main__':
    main()
