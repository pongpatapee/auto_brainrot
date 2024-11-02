import base64
import gzip
import json
import logging
import time
from abc import ABC, abstractmethod
from typing import override

import boto3
from botocore.exceptions import ClientError

AWS_KINESIS_STREAM_NAME = "autoBrainrotDataStream"

logger = logging.getLogger(__name__)

# class AbstractReader(ABC):
#     @abstractmethod
#     def read(self):
#         pass


class KinesisStreamReader:
    def __init__(self, aws_session: boto3.Session, aws_region="us-east-1") -> None:
        self.kinesis_client = aws_session.client("kinesis", region_name=aws_region)
        self.partition_key = "reddit"
        self.stream_name = AWS_KINESIS_STREAM_NAME

    def get_shard_iterator(self, shard_id, sharditeratortype="TRIM_HORIZON"):
        shard_iterator = self.kinesis_client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType=sharditeratortype,
        )["ShardIterator"]

        return shard_iterator

    def decompress_data(self, data):

        data_dict = json.loads(data.decode("utf8"))

        compressed_data_bytes = base64.b64decode(data_dict["data"])
        decompressed_data = gzip.decompress(compressed_data_bytes)

        return json.loads(decompressed_data)

    def get_records(self, starting_shard, max_records):
        record_count = 0
        try:
            shard_iter = self.get_shard_iterator(shard_id=starting_shard)
            while record_count < max_records:

                response = self.kinesis_client.get_records(
                    ShardIterator=shard_iter,
                    Limit=10,
                )

                shard_iter = response["NextShardIterator"]
                records = response["Records"]
                logger.info(f"Got {len(records)} records")
                record_count += len(records)

                yield records

        except ClientError:
            logger.exception(f"Couldn't get record from stream {self.stream_name}")
            raise


if __name__ == "__main__":
    from pprint import pprint

    aws_session = boto3.Session(profile_name="auto_brainrot")
    # kinesis_client = aws_session.client("kinesis", region_name="us-east-1")
    reader = KinesisStreamReader(aws_session)

    shard_id = "shardId-000000000000"
    records = reader.get_records(starting_shard=shard_id, max_records=1)
    for record in records:
        for data in record:
            pprint(data["Data"])
            print("Decompress")
            pprint(reader.decompress_data(data["Data"]))

        time.sleep(2)
