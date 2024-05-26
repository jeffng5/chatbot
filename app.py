from flask import Flask, render_template, request, flash, redirect, session, url_for, g
import requests, json
from playsound import playsound 
from forms import BioForm
import random
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = "it's a secret"


@app.route('/', methods=['GET'])
def home():
    form = BioForm()
    if form.validate_on_submit():
        name = form.username.data
        age = form.age.data
        sex = form.sex.data
        likes = form.likes.data
        interests = form.interests.data

        print("Hi `${name}`!")

    return render_template('home.html', form=form)


@app.route('/sidekick', methods=['GET'])
def intro():
    starter = {
        1: "How are you?",
        2: "What is your mood today?",
        3: "How is your day going?",
        4: "Do you have any questions for me?",
        5: "What is on your mind?"
    }
    list1 = [1, 2, 3, 4, 5]
    num = random.choice(list1)
    question = starter[num]

    response = session.get('response', None)
    transcription = session.get('transcription', None)
    responseURL = session.get('responseURL', None)

    
    return render_template('sidekick.html', question=question,
    response = response, transcription = transcription, responseURL=responseURL)
  


@app.route('/conversation', methods=['POST'])
def sidekick():

    def record():
        print('START RECORDING')

    #STEP 1 NEW :  recording your speech into an audio file
    # NEW AUDIO RECORDING METHOD (gets audio from client)
    ################################

        recording = request.files["audio"]
        recordingPath = "./static/jeff.wav"
       
        print('STOPPED')
        recording.save(recordingPath)

    #STEP 2 transcribing your audio file into text format
    ################################
        client = OpenAI(api_key=os.environ['API_KEY'])

        transcription = client.audio.transcriptions.create(model="whisper-1",
                                                       file=open(
                                                           recordingPath,
                                                           "rb"),
                                                            
        response_format='text')
        print(transcription)

    # STEP 3 fetching a response with your transcription from ChatGPT
    ################################
        completion = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user",                 "content": transcription}])
        completion = completion.choices[0].message
        responseText = completion.content
        print(responseText)

    #STEP 4 turning your response into a audio file
    ################################

        responsePath = "./static/speech.mp3"
        response = client.audio.speech.create(model='tts-1',
                                          voice='alloy',
                                          input=responseText)
        response.stream_to_file(responsePath)

    #STEP 5 playing the audio file
    ################################
  
    
        # session["responseURL"] = url_for("static", filename="speech.mp3")
        responseURL = "./static/speech.mp3"
        session['responseURL'] = responsePath
        session["response"] = responseText
        session["transcription"] = transcription
    
        
     
       
        # playsound(responsePath)
    record()
    return redirect('sidekick')
    
    

        
    
  
    
