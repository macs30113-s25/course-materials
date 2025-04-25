import boto3

# Initialize DynamoDB resource via boto3. To run code, be sure
# use LabRole IAM role to ensure Lambda can interact with DynamoDB
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    '''
    Test event (e.g. raw follower/tweet data for user):
    {
    "username": "john_doe",
    "followers": ["sally", "jim", "jane"],
    "tweets": ["this is a fun!", "Let's tweet some more."]
    }
    '''
    # reference existing table:
    table = dynamodb.Table('twitter')

    # process raw data to compute number of followers/tweets
    num_followers = len(event['followers'])
    num_tweets = len(event['tweets'])

    # then put processed data into DynamoDB table:
    table.put_item(
       Item={
            'username': event['username'],
            'num_followers': num_followers,
            'num_tweets': num_tweets
        }
    )

    return {'StatusCode': 200}
