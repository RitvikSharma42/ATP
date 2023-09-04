from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseBadRequest
from django.urls import reverse
from .models import AudioRecording
import subprocess
import os
import uuid

def record_audio(request):
    if request.method == 'POST':
        try:
            print("reaching record_audio")
            #print(request)
            audio_file = request.body
            if audio_file:
                print("Audio file present")
                recording = AudioRecording(audio_file=audio_file)
                #recording.save()
                #request.session['last_audio_id'] = recording.id
                #print(recording.id)
                #return JsonResponse({'message': 'Audio recorded successfully'})
                return render(request, 'run_script.html')
            else:
                return render(request, 'run_script.html')
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    return render(request, 'record_audio.html')

def run_script(request, audio_id):
    try:
        print("ok, reaching run_script")
        audio_recording = AudioRecording.objects.get(pk=audio_id)
        audio_file_path = audio_recording.audio_file.path

        script_output = subprocess.check_output(['python', 'atp_back2.py', audio_file_path])

        script_output = script_output.decode('utf-8')

        audio_recording.script_output = script_output
        audio_recording.save()

        return render(request, 'display_output.html', {'audioId': audio_id})

    except AudioRecording.DoesNotExist:
        return JsonResponse({'error': 'Audio recording not found'})

def display_output(request):
    last_audio_id = request.session.get('last_audio_id')

    if last_audio_id is not None:
        try:
            audio_recording = AudioRecording.objects.get(pk=last_audio_id)
            output_data = audio_recording.script_output

            return render(request, 'display_output.html', {'output_data': output_data})
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
