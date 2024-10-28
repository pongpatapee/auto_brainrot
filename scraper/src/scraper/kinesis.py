import base64
import gzip
import json
import sys
from abc import ABC, abstractmethod
from typing import override

import boto3
from models import KinesisRedditData, RedditPostContent

AWS_KINESIS_STREAM_NAME = "autoBrainrotDataStream"


class AbstractWriter(ABC):

    @abstractmethod
    def write(self, dst_name, data):
        pass


class KenesisStreamWriter(AbstractWriter):
    MAX_KINESIS_RECORD_SIZE = 1024 * 1024  # 1MiB

    def __init__(self, aws_session: boto3.Session, aws_region="us-east-1") -> None:
        self.kinesis_client = aws_session.client("kinesis", region_name=aws_region)
        self.partition_key = "reddit"

    def compress_data(self, data: KinesisRedditData):

        dict_data = data.model_dump()
        dict_data["data"] = gzip.compress(json.dumps(dict_data["data"]).encode("utf8"))
        dict_data["data"] = base64.b64encode(dict_data["data"]).decode("utf8")

        compressed_data = json.dumps(dict_data)

        return compressed_data

    @override
    def write(self, dst_name: str, data: KinesisRedditData):

        compressed_data = self.compress_data(data)

        data_size = sys.getsizeof(compressed_data)

        if data_size > self.MAX_KINESIS_RECORD_SIZE:
            return None

        response = self.kinesis_client.put_record(
            StreamName=dst_name, Data=compressed_data, PartitionKey=self.partition_key
        )

        return response


if __name__ == "__main__":
    writer = KenesisStreamWriter(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
    )

    data = KinesisRedditData(
        version="1.0",
        id="ligmaballs",
        data=RedditPostContent(
            title="bazinga", body="your mom sees the back of my head"
        ),
    )

    response = writer.write(dst_name=AWS_KINESIS_STREAM_NAME, data=data)

    print("writer response:")
    print(response)
