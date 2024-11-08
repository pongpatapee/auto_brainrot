from airflow.decorators import task
import boto3
import os

from orchestrator.constants import DATA_FOLDER
from speech.synthesizers.aws_speech_synthesizer import AwsSpeechSythesizer
from speech.inputs.tts_input import TtsInput

@task
def polly_tts_task(output_path: str):
    if output_path is None or len(output_path.strip()) == 0:
        raise ValueError("The argument 'output_path' cannot be None.")


    synthesizer = AwsSpeechSythesizer(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
        aws_region=os.getenv("AWS_REGION"),
    )

    tts_input = TtsInput(
        title="Sample Title",
        body="This is the body of the text for speech synthesis. Dan suck big peeeeeeeeen",
    )

    synthesizer.text_to_speech(input=tts_input, output_path=os.path.join(DATA_FOLDER, "output.mp3"))
