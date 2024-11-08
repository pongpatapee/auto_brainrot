import os

import boto3
from inputs.tts_input import TtsInput
from synthesizers.aws_speech_synthesizer import AwsSpeechSythesizer
from constants import DATA_FOLDER


def main():
    synthesizer = AwsSpeechSythesizer(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
        aws_region=os.getenv("AWS_REGION"),
    )

    tts_input = TtsInput(
        title="Sample Title",
        body="This is the body of the text for speech synthesis. Dan suck big peeeeeeeeen",
    )

    synthesizer.text_to_speech(input=tts_input, output_path=os.path.join(DATA_FOLDER, "output.mp3"))


if __name__ == "__main__":
    main()
