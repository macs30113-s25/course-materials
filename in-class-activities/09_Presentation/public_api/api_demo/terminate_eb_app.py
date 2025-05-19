import boto3
import time
from botocore.exceptions import ClientError

eb = boto3.client('elasticbeanstalk')
s3 = boto3.client('s3')

# Config details for EB app + env
app_name = 'books-api'
env_name = 'books-api-env'

# Terminate Environment
try:
    print(f"Terminating environment '{env_name}'.")
    eb.terminate_environment(EnvironmentName=env_name, ForceTerminate=True)
    print(f"Waiting for environment '{env_name}' to terminate...")
    while True:
        envs = eb.describe_environments(EnvironmentNames=[env_name], 
                                        IncludeDeleted=False)['Environments']
        if not envs:
            print("Environment terminated.")
            break
        time.sleep(10)
except ClientError as e:
    if "No Environment found" in str(e):
        print(f"Environment '{env_name}' does not exist. Skipping termination.")
    else:
        raise

# Delete all application versions
versions = eb.describe_application_versions(ApplicationName=app_name
                                            )['ApplicationVersions']
for version in versions:
    version_label = version['VersionLabel']
    print(f"Deleting application version '{version_label}'.")
    try:
        eb.delete_application_version(
            ApplicationName=app_name,
            VersionLabel=version_label
        )
    except ClientError as e:
        print(f"Could not delete version '{version_label}': {e}")

# Delete application
try:
    print(f"Deleting application '{app_name}'.")
    eb.delete_application(ApplicationName=app_name, TerminateEnvByForce=True)
except ClientError as e:
    if "No Application named" in str(e):
        print(f"Application '{app_name}' does not exist. Skipping deletion.")
    else:
        raise