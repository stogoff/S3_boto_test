
## S3 download/upload with 2 AWS accounts using boto3

#### Prepare your AWS
We have 2 AWS accounts.
On the first account, we should go to the AWS Management console, 
service S3 and create a new bucket.
Add its name in the field 'bucket1' of file config.py. 
Copy ID of the first account to the field 'account1_id'.
Go to IAM and create this policy (change <BUCKET> to new bucket's name) 
and save it as 'policy1':

```
policy1:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::<BUCKET>/*",
                "arn:aws:s3:::<BUCKET>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:HeadBucket"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}
```

Next, create a user with 'policy1'. 
Credentials of this user we'll copy to file config.py, 
in fields 'key' and 'secret'.
Upload the sample file to the bucket and add its name 
in the field 'remote_fn' of file config.py.

Next, we should go to the second account, copy its ID 
in the field 'account2_id', create new S3 bucket, 
add its name in the field 'bucket2',
create IAM role with type "Another AWS Account" 
adding account1_id as a parameter and copy its name 
in the field 'role', attach to the role policy AmazonS3FullAccess 

#### Use script
```python3 s3_down_up.py```




 