from django.shortcuts import render

from .models import *

from .forms import *
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import joblib
import numpy as np
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

from django.http import JsonResponse

#superuser: admin; password:admin

import requests
import json


def user(request):
    context = {}
    return render(request, 'aid/user.html', context)


def ambulance(request):
    ambulances = Ambulance.objects.all()
    available_ambulances = Ambulance.objects.filter(status="Available")
    available_count = available_ambulances.count()
    context = {
        'ambulances': ambulances,
        'available_ambulances': available_ambulances,
        'available_count': available_count
    }
    return render(request, 'aid/ambulance.html', context)


def spec_ambulance(request, pk):
    ambulance = Ambulance.objects.get(id=pk)
    context = {'ambulance': ambulance}
    return render(request, 'aid/specAmbulance.html', context)


def hospital(request):
    hospitals = Hospital.objects.all()
    available = hospitals.filter(status='Available')
    available_count = available.count()
    context = {'hospitals': hospitals, 'available': available,
               'available_count': available_count}

    return render(request, 'aid/hospital.html', context)


def spec_hospital(request, pk):
    hospital = Hospital.objects.get(id=pk)
    all_docs = Doctor.objects.filter(hospital=hospital)
    doc_no = all_docs.count()
    ambulances = Ambulance.objects.filter(hospital=hospital)
    context = {'hospital': hospital,
               'all_docs': all_docs,
               'ambulances': ambulances,
               'doc_no': doc_no}

    return render(request, 'aid/spechospital.html', context)


def driver(request):
    context = {}
    return render(request, 'aid/driver.html', context)


def doctor(request):
    doctors = Doctor.objects.all()
    available_doctors = Doctor.objects.filter(status="Available")
    available_count = available_doctors.count()
    context = {
        'doctors': doctors,
        'available_doctors': available_doctors,
        'available_count': available_count,
    }
    return render(request, 'aid/doctor.html', context)


def spec_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {'doctor': doctor}
    return render(request, 'aid/specDoctor.html', context)


def login(request):
    context = {}
    return render(request, 'aid/login.html', context)

# Create your views here.


def traffic(lat, lon):
    TRAFFIC_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml?key=######################&point="
    URL = TRAFFIC_URL+str(lat)+","+str(lon)
    response = requests.get(URL)
    if response.status_code == 200:
        # soup= BeautifulSoup(response.content,'xml')
        # print(soup.find_all('flowSegmentData'))
        with open('data.xml', 'wb')as f:
            f.write(response.content)
        tree = ET.parse("data.xml")
        root = tree.getroot()
        speed_element = root.findall("freeFlowSpeed")
        for value in speed_element:
            speed = value.text
        block_element = root.findall("roadClosure")
        for value in block_element:
            block = value.text

        # getting the main dict block
    #     main = data['main']
    #     speed=main['currentSpeed']
    #     block=main['roadClosure']
    #     print("Possible speed: ", speed)
    #     print("Any road blocks: ", block)
    # else:
    #     print("Error in HTTP request")

    return speed, block


def weather(lat, lon):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API = "#####################"
    URL = BASE_URL+"lat="+lat+"&lon="+lon+"&appid="+API
    response = requests.get(URL)
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['temp']
        # getting the humidity
        humidity = main['humidity']
        # weather report
        report = data['weather']
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print(f"Weather Report: {report[0]['description']}")
    else:
       # showing the error message
        print("Error in the HTTP request")

    if report[0]['description'].lower() == 'rain' or report[0]['description'].lower() == 'moderate rain':
        res = 2
    elif report[0]['description'].lower() == 'thunderstorm':
        res = 3
    elif report[0]['description'].lower() == 'snow':
        res = 4
    else:
        res = 1

    return res


def distance(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return(c * r)


def nlp_calc(details):
    model = load_model('nlp.h5')
    review = re.sub('[^a-zA-Z]', ' ', details)
    review.lower()

    vocab_size = 100
    max_length = 100
    trunc_type = 'post'
    oov_tok = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(review)
    sequences = tokenizer.texts_to_sequences(review)
    padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type)
    old = model.predict(padded)
    s = old.tolist()
    x = s[0]
    print(x)
    result = x.index(max(x))+1

    return result


def assign_calc(arr):
    model = joblib.load('assign.sav')
    res = model.predict([arr])

    return res[0]


def aid_assigner(request, latitude, longitude, details, h_assigned, a_assigned):
    aid = Aid.objects.create(
        latitude=latitude,
        longitude=longitude,
        aid_details=details,
        status="Ambulance Assigned"
    )
    Hospital.objects.filter(pk=h_assigned).update(status="Not Available")
    Ambulance.objects.filter(pk=a_assigned).update(
        status="Aid assigned",
        hosp_assgn=True,
        hospital=h_assigned)
    # doctors=Doctor.objects.filter(hospital=h_assigned, status="Available")
    # for doctor in doctors:
    #     doctor.update(status="Busy")
    #     break
        
def create_aid(request):
    assignFlag = False
    assignHospFlag = False
    form = AidForm()
    if request.method == 'POST':
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        details = request.POST.get("aid_details")
        now = datetime.now()
        print("Time: ", now.hour)

        hospitals = Hospital.objects.filter(status="Available")
        if hospitals:
            print(hospitals)
            assignHospFlag = True
            mini = float('inf')
            for hospital in hospitals:
                temp_d = distance(float(latitude), float(longitude), float(
                    hospital.latitude), float(hospital.longitude))
                if temp_d < mini:
                    mini = temp_d
                    h_assigned = hospital.id
                    print(h_assigned)
                    h_latitude = hospital.latitude
                    h_longitude = hospital.longitude
            if assignHospFlag:
                print("Hospital: ")
                print("Latitude: ", h_latitude)
                print("Longitude: ", h_longitude)
        else:
            print("No hospitals available !")

        ambulances = Ambulance.objects.filter(status="Available")

        for ambulance in ambulances:
            mini = float('inf')
            temp_d = distance(float(latitude), float(longitude), float(
                ambulance.latitude), float(ambulance.longitude))
            if temp_d < mini:
                mini = temp_d
                a_assigned = ambulance.id
                a_latitude = ambulance.latitude
                a_longitude = ambulance.longitude

        print("Ambulance: ")
        print("Latitude: ", a_latitude)
        print("longitude: ", a_longitude)

        nlp = nlp_calc(details)
        print("NLP result: ", nlp)
        de = distance(float(latitude), float(
            longitude), a_latitude, a_longitude)
        print("Distance to emergency: ", round(de, 3), "kms")
        da = distance(float(latitude), float(
            longitude), h_latitude, h_longitude)
        print("Distance to hospital: ", round(da, 3), "kms")
        total_distance = round(de+da, 3)
        print("Total distance: ", total_distance, "kms")
        wea = weather(latitude, longitude)
        e_speed, e_block = traffic(latitude, longitude)
        a_speed, a_block = traffic(a_latitude, a_longitude)
        h_speed, h_block = traffic(h_latitude, h_longitude)

        print("Speed at Emergency:", e_speed, "\tSpeed at ambulance:",
              a_speed, "\tSpeed at hospital:", h_speed)
        optimal_speed = (int(e_speed)+int(a_speed)+int(h_speed))/3
        time_taken = total_distance/optimal_speed
        time_final = round((time_taken*60), 1)
        print("Time taken:", time_final+5)
        parser = []
        parser.append(de)
        parser.append(da)
        parser.append(wea)
        parser.append(optimal_speed)
        parser.append(nlp)
        assign_stat = assign_calc(parser)

        if assign_stat:
            assignFlag = True

        if assignFlag:
            print("Passed ML. Assigning !")
            aid_assigner(request, latitude, longitude,
                         details, h_assigned, a_assigned)

    context = {'form': form}
    return render(request, 'aid/createAid.html', context)
