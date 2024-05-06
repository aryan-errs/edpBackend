from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .helpers import create_assistant
from time import sleep
from openai import OpenAI
import base64
import tempfile
import whisper
from pydub import AudioSegment
from django.http import JsonResponse
import io
import json


class ChatView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client=OpenAI(api_key='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')
        self.model=None
        # self.assistant_id=create_assistant(self.client)
    def load_model(self):
        # Check if the model is already loaded in the cache
        if not self.model:
            # Load the model here
            self.model = whisper.load_model("tiny")

    def get_medical_advice(self,user_input):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical chatbot that diagnoses diseases. User will input in the form: Symptoms: \"....\", Pulse Rate: \"...\", Oxygen level: \"....\", Temperature: \".....\" , you have to provide output in the form: Predicted disease: \"....\" , Treatment Plan: \"....\", Prescribed Drugs: \"....\", Specialization: \"....\". Prescribe safe drugs based on treatment plan. For specialization, if treatment plan involves visiting a doctor, it specifies which specialization of doctor to visit. Also some inputs from user may be unknown, diagnose and provide output with rest known inputs."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content
    
    def put(self,request):
        audio_file = request.FILES.get('audio_data')
        if audio_file:
            audio_data = audio_file.read()
            audio_format = request.POST.get('type', 'wav')

            # Convert audio data to AudioSegment
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))

            # Save AudioSegment as MP3 file
            audio_segment.export('audio.mp3', format='mp3')

            return JsonResponse({'message': 'Audio file saved as MP3'})
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)


    def post(self,request):
        print(request.data)
        if not request.data['pulse_rate']:
            return Response({"message":"Please provide pulse_rate"},400)
        
        if not request.data['oxygen_level']:
            return Response({"message":"Please provide oxygen level"},400)
        
        if not request.data['temperature']:
            return Response({"message":"Please provide temperature"},400)

        pulse_rate=request.data['pulse_rate']
        oxygen_level=request.data['oxygen_level']
        temperature=request.data['temperature']
        symptoms=""
        if request.data['text']!="":
            symptoms=request.data['text']
        else:
            # Load the model
            self.load_model()
            print("Model loaded")
            result = self.model.transcribe("audio.mp3",language="english")
            print(f' The text in video: \n {result["text"]}')
            symptoms=result["text"]
        user_input = f"Symptoms: \"{symptoms}\", Pulse Rate: \"{pulse_rate}\", Oxygen level: \"{oxygen_level}\", Temperature: \"{temperature}\""


        advice = self.get_medical_advice(user_input)
        print("Advice:", advice)

    # Split the advice string to extract each attribute
        
        advice_attributes = advice.split("\n")
        if(len(advice_attributes)<4):
            res={"predicted_disease": None,"treatment_plan": None,"prescribed_drugs": None,"specialization": None}

            return Response({"message":res},200)
        
        print("Advice Attributes:", advice_attributes)
        predicted_disease = advice_attributes[0].split(": ")[1].strip('"').replace('",', '')
        treatment_plan = advice_attributes[1].split(": ")[1].strip('"').replace('",', '')
        prescribed_drugs = advice_attributes[2].split(": ")[1].strip('"').replace('",', '')
        specialization = advice_attributes[3].split(": ")[1].strip('"').replace('",', '')

        res={"predicted_disease": predicted_disease,"treatment_plan": treatment_plan,"prescribed_drugs": prescribed_drugs,"specialization": specialization}

        return Response({"message":res},200)
