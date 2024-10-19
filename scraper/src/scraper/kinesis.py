import json

import boto3

aws_session = boto3.Session(profile_name="auto_brainrot")
kinesis_client = aws_session.client("kinesis", region_name="us-east-1")

stream_name = "autoBrainrotDataStream"

# TODO: compress records via gzip
# If > 1MB throw away
record = {
    "reddit_post_title": "bazinga",
    "reddit_post_content": "Your mom sees the back of my head",
}

record_data = json.dumps(record)

response = kinesis_client.put_record(
    StreamName=stream_name, Data=record_data, PartitionKey="reddit"
)

print(f"Record sent to Kinesis: {response}")
