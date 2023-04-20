from requests import Session
from ..utils.b64utils import b64utils
from ..utils.string_utils import string_utils

import speech_recognition as sr
import time, os

class Captcha():
    def __init__(
            self,
            image_b64: str,
            correct_answ: str,
            init_vector: str,
            key: str,
            audio_b64: str
        ) -> None:
        self.image_b64 = image_b64
        self.correct_answ = correct_answ
        self.init_vector = init_vector
        self.key = key
        self.audio_b64 = audio_b64

        self.answer = ""
        pass

class mocap():

    def solve_audio(captcha: Captcha) -> str:
        file_name = string_utils.random_string(2)
        b64utils.b64_to_wav(base64_string=captcha.audio_b64, output_file_path=f"data/audio/{file_name}.wav")
        r = sr.Recognizer()
        r.energy_threshold = 0
        r.dynamic_energy_threshold = False
        r.non_speaking_duration = 0
        r.phrase_threshold = 0.0
        r.pause_threshold = 0
        with sr.WavFile(f"data/audio/{file_name}.wav") as source:
            audio = r.record(source)

        response = r.recognize_google(audio)
        answer = mocap._audio_transcription_to_text(transcription=response)

        # Remove the file because I have 3gb of wav files now
        os.remove(f"data/audio/{file_name}.wav")
        return answer
    
    def _audio_transcription_to_text(transcription: str) -> str:
        fixed_string = mocap._sanitize_input(transcription)
        words = fixed_string.split()
        output_string = ""

        # loop through each word in the input string
        for word in words:
            # if the word is a number, add it to the output string
            if word.isdigit():
                output_string += word
            # if the word is a letter, add its first letter to the output string
            else:
                output_string += word[0].upper()

        return output_string
    
    def _sanitize_input(input_string: str) -> str:

        # Sometimes the audio recognition will think the audio is saying a time, like 9:09.
        # This SHOULD fix it.
        input_string = input_string.replace(":", "")

        number_like_words = {
            "zero": "0",
            "oh": "0",
            "one": "1",
            "two": "2",
            "to": "2",
            "too": "2",
            "three": "3",
            "tree": "3",
            "four": "4",
            "fore": "4",
            "for": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "ate": "8",
            "nine": "9"
        }

        for word, digit in number_like_words.items():
            input_string = input_string.replace(word, digit)
        
        return input_string

    def retrieve_captcha(session: Session = Session()) -> Captcha:
        headers = {
            "Accept": "application/json"
        }
        resp = session.get(f"https://ago.mo.gov/RestApi/comments-api/captcha?_={int(time.time())}", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            image_b64 = data.get("Image")
            correct_answ = data.get("CorrectAnswer")
            init_vector = data.get("InitializationVector")
            key = data.get("Key")
            audio_b64 = data.get("Audio")

            return Captcha(
                image_b64=image_b64,
                correct_answ=correct_answ,
                init_vector=init_vector,
                key=key,
                audio_b64=audio_b64
            )
        else: return None