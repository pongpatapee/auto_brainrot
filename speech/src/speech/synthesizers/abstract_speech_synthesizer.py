from abc import ABC, abstractmethod

from models import TtsInput


class AbstractSpeechSynthesizer(ABC):

    @abstractmethod
    def text_to_speech(self, input: TtsInput):
        pass
