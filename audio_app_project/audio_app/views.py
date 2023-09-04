from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import AudioRecording
import subprocess
import os
import uuid
from atp_back2 import fin
import io
def record_audio(request):
    if request.method == 'POST':
        print("reaching record_audio")

        # Check if an audio file was uploaded
        if 'audioFile' in request.FILES:
            audio_file = request.FILES['audioFile']

            # Assuming you have a model named AudioRecording
            recordingt = AudioRecording(audio_file=audio_file)
            recordingt.save()

            path = recordingt.audio_file.path

            result= fin(path)
            print(result)
            request.session["result"]=result
            # You can return a response or redirect as needed
            return render(request, 'display_output.html',{"result":result})
        else:
            print("No audio file uploaded")

    return render(request, 'record_audio.html')



def display_output(request):
    
    result=request.session["result"]
    try:
        return render(request, 'display_output.html',{"result":result})
    except AudioRecording.DoesNotExist:
        return JsonResponse({'error': 'Audio recording not found'})

    return JsonResponse({'error': 'No recent audio recording found'})


def faq_view(request):
    faq_url = reverse('faq')
    context = {
        'faq_url': faq_url,
    }
    return render(request, 'faq.html', context)

import pandas as pd
from django.shortcuts import render

def product_list_view(request):
    excel_path = "/home/ubuntu/atp/django-ajax-record/final_cat.xlsx"

    try:
        df = pd.read_excel(excel_path)
        product_names = df.to_dict(orient='records')

    except Exception as e:
        print(e)
        product_names = []

    context = {
        'product_names': product_names,
    }
    return render(request, 'product_list.html', context)
