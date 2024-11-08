from abc import ABC, abstractmethod

from speech.inputs.tts_input import TtsInput


class AbstractSpeechSynthesizer(ABC):

    @abstractmethod
    def text_to_speech(self, input: TtsInput, output_path: str):
        pass
