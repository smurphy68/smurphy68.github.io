import routines
from routines import *

check_routines()
import speech_recognition as sr
from openai import OpenAI
from open_ai_secrets import OPENAI_API_KEY
import time
from pathlib import Path
import pygame
import json
import os
import inspect

def check_routines():
    routines.check_routines()

def get_function_info(module):
    function_info = {}
    members = inspect.getmembers(module)
    for name, member in members:
        if inspect.isfunction(member):
            argspec = inspect.getfullargspec(member)
            args = argspec.args
            defaults = argspec.defaults
            if not args:
                pass
            else:
                function_info[name] = {}
                if defaults:
                    ## Have to change if default values becomes a thing rather than "None"
                    function_info[name]["defaults"] = [arg for arg, default_value in
                                                       zip(reversed(args), reversed(defaults)) if
                                                       default_value is None]
                function_info[name]["required"] = args if not defaults else [arg for arg in args if
                                                                             arg not in function_info[name][
                                                                                 "defaults"]]
    return function_info

def create_prompt(command):
    functions = [os.path.splitext(file)[0] for file in os.listdir("routines") if file.endswith(".py")]
    string_functions = str(functions)
    arguments = get_function_info(routines)
    string_arguments = str(arguments)
    prompt = '''
        Generate a JSON string representing the appropriate function and arguments, make sure to return the JSON ONLY as a plain text response:
        {command}\n
        Available Functions:
        {functions}\n
        Variables:
        {arguments}\n
        '''.format(command=command, functions=string_functions, arguments=string_arguments)
    return prompt


def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()
    while True:
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            time.sleep(1)
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.mixer.quit()
            break


class Friday:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.thread_id = None

    def handle_command(self, command):
        prompt = create_prompt(command)
        response = self.process_command(prompt)
        print(response)
        if response == "nothing":
            print("Not a known command")
            return False
        else:
            # parse json
            response_dict = json.loads(response)
            if isinstance(response_dict, dict) and len(response_dict):
                function = response_dict["function"]
                args = None
                if len(response_dict) != 1:
                    args = response_dict["arguments"]
                output = self.get_resource(function, None if not args else args)
                return output

    def process_command(self, command):
        assistant = self.client.beta.assistants.retrieve(assistant_id="Steve")
        thread = self.client.beta.threads.create()
        if self.thread_id is None:
            self.thread_id = thread.id
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=command
        )
        run = self.client.beta.threads.runs.create(
            assistant_id=assistant.id,
            thread_id=self.thread_id
        )
        while True:
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            if run.status == "completed":
                break
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
        )
        response = messages.data[0].content[0].text.value
        return response

    def get_resource(self, function_name, arguments):
        function_name = function_name.strip(", ").strip(" ")
        if hasattr(routines, function_name):
            function = getattr(routines, function_name)
            if callable(function):
                if function == gpt_chat_response:
                    result = function(**arguments)
                    self.open_ai_tts(result)
                    return
                if arguments:
                    result = function(**arguments)
                else:
                    result = function()
                return result
            else:
                print(f"Object '{function_name}' in the module is not callable.")
        else:
            print(f"Function '{function_name}' not found in the module.")

    def open_ai_tts(self, text, file_path="response.mp3"):
        speech_file_path = Path(__file__).parent / file_path
        speech = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="fable",
            input=text
        )
        speech.stream_to_file(speech_file_path)
        play_audio(speech_file_path)

    def detect_keyword(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("[EVENT] Listening for 'Hey, Friday'...")
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "friday" in command and "hey" in command:
                    pygame.mixer.quit()
                    self.handle_command(command)
            except sr.UnknownValueError:
                print("[EVENT] Sorry, could not understand audio.")
            except sr.RequestError as e:
                print(f"[EVENT] Error during offline speech recognition; {e}")

    def run(self):
        while True:
            try:
                self.detect_keyword()
            except Exception as e:
                print(f"Exception: {e}")
                raise e


if __name__ == "__main__":
    friday = Friday()
    friday.run()
