from flask import Flask, render_template, request, flash, redirect, session, g
import requests, json
import json
from forms import BioForm
import random
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os
from playsound import playsound
from pathlib import Path


app = Flask(__name__)

app.config['SECRET_KEY'] = "it's a secret"

@app.route('/', methods =['GET', 'POST'])
def home():
    form = BioForm()
    if form.validate_on_submit():
        name = form.username.data
        age = form.age.data
        sex= form.sex.data
        likes= form.likes.data
        interests = form.interests.data
        
        print("Hi `${name}`!")

    return render_template('home.html', form=form)

@app.route('/sidekick', methods = ['GET'])
def intro():
    starter = {
    1: "how are you?",
    2: "what is your mood today?",
    3: "how is your day going?",
    4: "do you have any questions for me?",
    5: "what is on your mind?"
}
    list1 = [1,2,3,4,5]
    num = random.choice(list1)
    question = starter[num]
    
    return render_template('sidekick.html', question=question)
    
    
@app.route('/conversation', methods=['GET'])
def sidekick():
    
#STEP 1 :  recording your speech into an audio file 
    def record(): 
        print('START RECORDING')
        # Sampling frequency
        frequency = 44400
 
        # Recording duration in seconds
        duration = 6
 
        # to record audio from sound-device into a Numpy
        recording = sd.rec(int(duration * frequency),
                   samplerate = frequency, channels = 1)
 
        # Wait for the audio to complete
        sd.wait()
 
        # using scipy to save the recording in .wav format
        # This will convert the NumPy array
        # to an audio file with the given sampling frequency
        write("jeff.wav", frequency, recording)
 
        # using wavio to save the recording in .wav format
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        wv.write("jeffrey.wav", recording, frequency, sampwidth=2)
       
        return (print('DONE'))

    record()
    
#STEP 2 transcribing your audio file into text format    
    client = OpenAI(api_key = 'sk-proj-cBud2OD12T1i7x6d7UiAT3BlbkFJ0f5q9sH9htWwH7ExeNab')

    audio_file = open("/Users/Spare/Chatbot/jeffrey.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format='text')
    print(transcription)
    reply = transcription
    
#STEP 3 fetching a response with your transcription from ChatGPT        
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role": "user", "content": transcription}]
    )
    completion = completion.choices[0].message
    answer = completion.content
    print(answer)
    
#STEP 4 turning your response into a audio file
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model='tts-1',
        voice='alloy',
        input= completion.content
    )
    response.stream_to_file(speech_file_path)
    
#STEP 5 playing the audio file
    playsound('/Users/Spare/Chatbot/speech.mp3')
        
    return render_template('sidekick.html',reply=reply, answer=answer)
            
        
    
  
    
