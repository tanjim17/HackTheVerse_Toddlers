from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Doctor, Nurse, Reception, Bed
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from patient.models import *
import datetime
import random

def check_usertype(request):
    if request.user.is_authenticated:
        if Doctor.objects.filter(user=request.user.id).exists():
            return 'doctor', Doctor.objects.get(user=request.user.id)
        elif Nurse.objects.filter(user=request.user.id).exists():
            return 'nurse', Nurse.objects.get(user=request.user.id)
        elif Reception.objects.filter(user=request.user.id).exists():
            return 'reception', Reception.objects.get(user=request.user.id)
        else:
            return 'admin', ' '
    else:
        return ' ', ' '

def home_page(request):
    return render(request, 'home.html')

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                # Handle Failed Login
                return HttpResponse("Invalid login details supplied.")

        return render(request, 'login.html')
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def dashboard(request):

    usertype, user = check_usertype(request)

    if usertype == 'doctor':

        beds = Bed.objects.all().filter(doctor_fk=Doctor.objects.get(user=request.user.id))
        allpatients = []
        for bed in beds:
            patients = Patient.objects.all().filter(bed=bed)
            for patient in patients:
                allpatients.append([patient.patientID, patient.name])
        return render(request, 'doctorDashboard.html', {'allpatients': allpatients})

    elif usertype == 'nurse':
        beds = Bed.objects.all().filter(nurse_fk=Nurse.objects.get(user=request.user.id))
        allpatients = []
        for bed in beds:
            patients = Patient.objects.all().filter(bed=bed)
            for patient in patients:
                allpatients.append([patient.patientID, patient.name])
        return render(request, 'nurseDashboard.html', {'allpatients': allpatients})

    elif usertype == 'reception':

        if request.method == 'POST':
            formIdentity = request.POST.get('formIdentity')

            if formIdentity == 'register':
                name = request.POST.get('patientname')
                age = int(request.POST.get('patientage'))
                gender = request.POST.get('patientgender')

                beds_taken = []
                patientIDs = []
                for i in Patient.objects.all():
                    beds_taken.append(i.bed.bedID)
                    patientIDs.append(i.patientID)

                for i in PreviousPatient.objects.all():
                    patientIDs.append(i.patientID)
                patientIDs.sort(reverse=True)

                available_beds = []
                for i in Bed.objects.all():
                    if i.bedID not in beds_taken:
                        available_beds.append(i.bedID)
                available_beds.sort()

                if len(available_beds)>0:
                    bed = Bed.objects.get(bedID=available_beds[0])
                    if len(patientIDs) == 0:
                        id = 1
                    else:
                        id = patientIDs[0]+1
                    patient = Patient.objects.create(age=age, name=name, gender=gender, admissionDate=datetime.datetime.now(), patientID=id, bed=bed)

            elif formIdentity == 'discharge':
                patientid = int(request.POST.get('patientid'))
                patient = Patient.objects.get(patientID=patientid)
                previousPatient = PreviousPatient.objects.create(patientID=patient.patientID, gender=patient.gender, age=patient.age, name=patient.name, admissionDate=patient.admissionDate, bed=patient.bed, releaseData=datetime.datetime.now())
                previousPatient.save()
                patient.delete()

            return HttpResponseRedirect(reverse('dashboard'))

    elif usertype == 'admin':
        return HttpResponseRedirect('http://{}/admin'.format(request.META['HTTP_HOST']))

    return render(request, 'receptionDashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

# def populate():
#     return
    # Populate with Doctors
    # for i in range(5):
    #
    #     username = 'D'+str(i+1)
    #     password = '1234'
    #     doctorID = i
    #     name = 'Doctor ' + str(i+1)
    #
    #     user = User.objects.create(username=username)
    #     user.set_password(password)
    #     user.save()
    #     doctor = Doctor.objects.create(doctorID=doctorID, user=user, name=name)
    #     doctor.save()

    # Populate with Nurses
    # for i in range(20):
    #     username = 'N' + str(i+1)
    #     password = '1234'
    #     nurseID = i
    #     name = 'Nurse ' + str(i+1)
    #
    #     user = User.objects.create(username=username)
    #     user.set_password(password)
    #     user.save()
    #     nurse = Nurse.objects.create(nurseID=nurseID, user=user, name=name)
    #     nurse.save()

    # Populate with Beds
    # for i in range(100):
    #     doctorID = i//20
    #     nurseID = i//5
    #     doctor = Doctor.objects.get(doctorID=doctorID)
    #     nurse = category_id = Nurse.objects.get(nurseID=nurseID)
    #     Bed.objects.create(doctor_fk=doctor, nurse_fk=nurse, bedID=i, floor=i//20+1, roomNo=i//5+1)

    # Populate Reception
    # for i in range(2):
    #     username = 'R' + str(i+1)
    #     password = '1234'
    #     receptionID = i
    #     name = 'Reception ' + str(i+1)
    #
    #     user = User.objects.create(username=username)
    #     user.set_password(password)
    #     user.save()
    #     reception = Reception.objects.create(receptionID=receptionID, user=user, name=name)
    #     reception.save()

@login_required
def patient_details(request , patient_id):
    usertype, user = check_usertype(request)
    if usertype == 'doctor' or usertype == 'nurse':
        p_obj = Patient.objects.get( patientID = patient_id).__dict__
        bedid = p_obj['bed_id']

        "p_obj['recent'] = RecentMedicalData.objects.get(bed_id = bedid).__dict__"
        #p_obj['historical'] = HistoricalMedicalData.objects.get(bed_id=bedid).__dict__

        p_obj['body_temp_graph'] =  temp_graph()
        p_obj['bp_graph'] = bp_graph()

        return render(request, 'patientdetails.html' , p_obj)
    elif usertype == 'reception':
        return HttpResponseRedirect(reverse('dashboard'))

@login_required
def update_patient_details(request):
    usertype, user = check_usertype(request)
    patient_id = request.GET['patient_id']
    if usertype == 'doctor' or usertype == 'nurse':
        bedid = Patient.objects.get(patientID=patient_id).bed
        r_objs = RecentMedicalData.objects.all().filter(bed_id=bedid)
        recents = []
        for r_obj in r_objs:
            recents.append([r_obj.timestamp, r_obj.heartrate, r_obj.body_temp, r_obj.oxygen_level])
        return JsonResponse({'recents': recents})
    elif usertype == 'reception':
        return HttpResponseRedirect(reverse('dashboard'))


import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

def temp_graph():
    x = np.arange(1, 31)
    y = []
    for i in range(1, 31):
        y.append(random.randint(98, 104))

    fig, ax1 = plt.subplots(figsize = (12,5))
    ax1.plot(x, y, lw=2, color="red")
    plt.title('Change in body temperature(^oC) over the last month',
              fontsize=14, fontweight='bold')
    ax1.set_ylabel(r"Body Tempeature $(^oC)$", fontsize=12, color="blue")
    for label in ax1.get_yticklabels():
        label.set_color("green")
    for label in ax1.get_xticklabels():
        label.set_color("green")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def bp_graph():
    x = np.arange(1, 31)
    ysys = []
    ydia = []
    for i in range(1, 31):
        ysys.append(random.randint(110, 180))

    for i in range(1, 31):
        ydia.append(random.randint(50 , 105))

    fig, ax1 = plt.subplots(figsize = (12,5))
    ax1.plot(x, ysys, lw=2, color="blue")
    plt.title('Change in BP over the last month',
              fontsize=14, fontweight='bold')
    ax1.set_ylabel(r"Systolic BP", fontsize=12, color="blue")
    for label in ax1.get_yticklabels():
        label.set_color("green")
    for label in ax1.get_xticklabels():
        label.set_color("green")

    ax2 = ax1.twinx()
    ax2.plot(x, ydia, lw=2, color="red")
    ax2.set_ylabel(r"Diastolic BP", fontsize=12, color="red")
    for label in ax2.get_yticklabels():
        label.set_color("red")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


"""
    fig = plt.figure(figsize=(12,5))
    plt.title('Change in body temperature(^oC) over the last month',
              fontsize=14, fontweight='bold')
    plt.plot(x,y)
"""
