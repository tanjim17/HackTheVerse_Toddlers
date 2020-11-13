from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Doctor, Nurse, Reception, Bed
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def check_usertype(request):
    if request.user.is_authenticated:
        if Doctor.objects.filter(user=request.user.id).exists():
            return 'doctor', Doctor.objects.get(user=request.user.id)
        elif Nurse.objects.filter(user=request.user.id).exists():
            return 'nurse', Nurse.objects.get(user=request.user.id)
        elif Reception.objects.filter(user=request.user.id).exists():
            return 'reception', Reception.objects.get(user=request.user.id)
    else:
        return ' ', ' '

# Create your views here.
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

def populate():
    return
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
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def dashboard(request):

    usertype, user = check_usertype(request)

    if usertype == 'doctor':
        return render(request, 'doctorDashboard.html')

    elif usertype == 'nurse':
        return render(request, 'nurseDashboard.html')

    elif usertype == 'reception':

        if request.method == 'POST':
            formIdentity = request.POST.get('formIdentity')

            if formIdentity == 'register':
                name = request.POST.get('patientname')
                age = int(request.POST.get('patientage'))
                gender = request.POST.get('patientgender')
                
            elif formIdentity == 'discharge':
                age = int(request.POST.get('patientid'))

            return HttpResponseRedirect(reverse('dashboard'))

        return render(request, 'receptionDashboard.html')
