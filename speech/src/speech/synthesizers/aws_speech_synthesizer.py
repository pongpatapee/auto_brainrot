import os
from io import BytesIO

import boto3
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError
from constants import DATA_FOLDER
from inputs.tts_input import TtsInput
from synthesizers.abstract_speech_synthesizer import AbstractSpeechSynthesizer
from typing_extensions import override

AWS_POLLY_CLIENT_NAME = "polly"


class AwsSpeechSythesizer(AbstractSpeechSynthesizer):
    # TODO(isaeed): add configs when this is flushed.
    def __init__(self, aws_session: boto3.Session, aws_region="us-east-1") -> None:
        self.polly_client: BaseClient = aws_session.client(
            AWS_POLLY_CLIENT_NAME,
            region_name=aws_region,
        )

    @override
    def text_to_speech(self, input: TtsInput):
        try:
            # Call Amazon Polly to synthesize speech
            response = self.polly_client.synthesize_speech(
                Text=input.body,
                OutputFormat="mp3",  # You can change this to other formats like 'ogg_vorbis', 'pcm', etc.
                VoiceId="Brian",  # British English voice
                LanguageCode="en-GB",  # Language code for British English
            )

            # Access the audio stream from the response
            audio_stream = response["AudioStream"]

            # Save or process the audio stream as needed
            audio_bytes = BytesIO(audio_stream.read())
            audio_stream.close()

            # Here you can save it to a file or play it directly, for example:
            with open(os.path.join(DATA_FOLDER, "output.mp3"), "wb") as file:
                file.write(audio_bytes.getbuffer())

            print("Audio content written to output.mp3")

        except (BotoCoreError, ClientError) as error:
            print(f"An error occurred: {error}")
