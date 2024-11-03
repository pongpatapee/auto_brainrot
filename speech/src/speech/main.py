import os
import time
from pprint import pprint

import boto3
from models import TtsInput
from readers.kinesis import KinesisStreamReader
from synthesizers.aws_speech_synthesizer import AwsSpeechSythesizer


def main():

    synthesizer = AwsSpeechSythesizer(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
    )

    reader = KinesisStreamReader(
        aws_session=boto3.Session(profile_name="auto_brainrot")
    )

    shard_id = "shardId-000000000000"
    records = reader.get_records(starting_shard=shard_id, max_records=1)
    for record in records:
        for data in record:
            reddit_data = reader.decompress_data(data["Data"])
            print("Decompressed Data")
            print(reddit_data)

            tts_input = TtsInput.model_validate(reddit_data)

            synthesizer.text_to_speech(tts_input)

        time.sleep(2)


if __name__ == "__main__":
    main()
