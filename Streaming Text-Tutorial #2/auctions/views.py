from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import speech_recognition as sr
import keyboard
from openai import OpenAI
import pyttsx3


def index(request):
    return render(request, "auctions/index.html")


def stream(request):
    #def event_stream():
    #    ex_text = ["Akshat: Hi", "Chatbot: How are you doing", "Akshat: Bye"]
        #while True:
    response = StreamingHttpResponse(messages([], request), content_type="text/event-stream")
    response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
    response['Cache-Control'] = 'no-cache'  # Ensure clients don't cache the data
    return response


def messages(conversation_transcript, request):
    user_name = "USER: "
    chatbot_name = "ECHO: "

    recognizer = sr.Recognizer()
    client = OpenAI(
        api_key="PUT API KEY HEREgit status",
    )
    final_list = []
    conversation_transcript = ['','']
    system_msg = f"You are a friendly assistant in a todo list app that is doing an end of day check in for the user's tasks.\nExisting to-do list: {''.join(final_list)}"
    engine = pyttsx3.init()
    # engine.setProperty("rate", 200)
    engine.setProperty("volume", 1)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)

    while True:
        with sr.Microphone() as source:
            print("\ncUSER: ")
            audio = recognizer.listen(source)
            #print(audio)

        # text = ""

        print("converting to text")
        text = recognizer.recognize_whisper(audio, language="en")
        #print(text)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_msg
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="gpt-3.5-turbo",
        )

        assistant_message = chat_completion.choices[0].message.content
        #print("\nECHO: " + assistant_message)
        conversation_transcript[1] = chatbot_name + assistant_message
        engine.say(assistant_message)
        for item in conversation_transcript:
            print(item)
            #data = json.load(item)
            yield f'data: {item}\n\n'
        engine.runAndWait()
        if keyboard.is_pressed('q'):
            break
