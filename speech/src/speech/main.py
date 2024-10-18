import os

import boto3
from constants import ROOT_DIR
from dotenv import load_dotenv
from inputs.tts_input import TtsInput
from synthesizers.aws_speech_synthesizer import AwsSpeechSythesizer


def main():
    # loaded_at_least_one: bool = load_dotenv()
    # if not loaded_at_least_one:
    #     raise RuntimeError("Couldn't load env variables")

    synthesizer = AwsSpeechSythesizer(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
        aws_region=os.getenv("AWS_REGION"),
    )

    tts_input = TtsInput(
        title="Sample Title",
        body="This is the body of the text for speech synthesis. Dan suck big peeeeeeeeen",
    )

    synthesizer.text_to_speech(tts_input)


if __name__ == "__main__":
    main()
