import boto3
import time
from botocore.exceptions import ClientError

# Initialize clients
s3 = boto3.client('s3')
eb = boto3.client('elasticbeanstalk')

# Config details for EB app + env, S3 bucket + key where zipped app is located
app_name = 'books-api'
env_name = 'books-api-env'
s3_bucket = 'css-uchicago' # upload a zip to your own S3 bucket to modify app
zip_s3_key = 'api.zip'

# Create application if it doesn't already exist
try:
    print(f"Creating application '{app_name}'...")
    eb.create_application(ApplicationName=app_name, Description='Books API')
    print("Application created.")
except ClientError as e:
    error_code = e.response['Error']['Code']
    error_msg = e.response['Error']['Message']

    if error_code == 'InvalidParameterValue' and 'already exists' in error_msg:
        print(f"Application '{app_name}' already exists. Skipping creation.")
    else:
        raise

# Create a new application version based on current time, using zipped app
version_label = f"v-{int(time.time())}"
print(f"Creating application version {version_label}.")
eb.create_application_version(
    ApplicationName=app_name,
    VersionLabel=version_label,
    SourceBundle={
        'S3Bucket': s3_bucket,
        'S3Key': zip_s3_key
    },
    Process=True
)

# Wait for app version to finish processing before proceeding
timeout = time.time() + 60
while time.time() < timeout:
    versions = eb.describe_application_versions(
        ApplicationName=app_name,
        VersionLabels=[version_label]
        )['ApplicationVersions']
    status = versions[0]['Status']
    if versions and status == 'PROCESSED':
        break
    time.sleep(5)

# Check if environment (a running deployment of an application version) exists
envs = eb.describe_environments(ApplicationName=app_name, 
                                EnvironmentNames=[env_name],
                                IncludeDeleted=False)['Environments']
if envs:
    # Update existing environment
    print(f"Updating environment '{env_name}' with new version.")
    eb.update_environment(
        EnvironmentName=env_name,
        VersionLabel=version_label
    )
else:
    # Create new environment
    print(f"Creating new environment '{env_name}'.")
    eb.create_environment(
        ApplicationName=app_name,
        EnvironmentName=env_name,
        VersionLabel=version_label,
        SolutionStackName='64bit Amazon Linux 2023 v4.5.1 running Python 3.9',
        OptionSettings=[
            {
            'Namespace': 'aws:autoscaling:launchconfiguration',
            'OptionName': 'IamInstanceProfile',
            'Value': 'LabInstanceProfile'
        },
            {
            'Namespace': 'aws:elasticbeanstalk:environment',
            'OptionName': 'ServiceRole',
            'Value': 'LabRole'
        }
        ]
    )

# Wait for environment to be ready
print(f"Waiting for environment '{env_name}' to be ready...")
timeout = time.time() + 300 # wait for up to 5 minutes
while time.time() < timeout:
    env = eb.describe_environments(ApplicationName=app_name, 
                                EnvironmentNames=[env_name], 
                                IncludeDeleted=False)['Environments'][0]
    # check status every 10s until ready:
    status = env['Status']
    health = env.get('Health', 'UNKNOWN')
    if status == "Ready" and health in ["Green", "Yellow"]:
        print(f"Environment is ready. Public URL: Public URL: http://{env['CNAME']}")
        break
    time.sleep(10)