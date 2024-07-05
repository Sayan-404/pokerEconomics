import os
import traceback

import boto3
from dotenv import load_dotenv

load_dotenv()

# Accessing the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
aws_instance = os.getenv('AWS_INSTANCE')


def shutdownInstance():
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        ec2 = session.client('ec2')
        ec2.stop_instances(InstanceIds=[aws_instance])
        print(f"Instance {aws_instance} is shutting down.")
    except Exception as e:
        print(f"Failed to shut down instance: \n{traceback.print_exc()}")
