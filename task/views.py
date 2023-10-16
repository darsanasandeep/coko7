import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import requests
# Create your views here.
from task.forms import RegisterForm
from task.models import UserTask, UserProfile


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(user_login)
    return render(request,'register.html',{'form':form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passw']
        user = authenticate(username=username,password=passwd)
        if user is not None:
            login(request,user)
            return redirect(Dashboard)
        else:
            return redirect(user_login)
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect(user_login)

def AddTask(request):

    if request.method == 'POST':
        task = request.POST['task']
        due = request.POST['due']
        descp = request.POST['descp']
        user_id = request.user.id
        start_date = datetime.datetime.today()
        data = UserTask.objects.create(user_id=user_id,task_name=task,start_date=start_date,due_date=due,discrp=descp,status='pending')
        data.save()
        return redirect(ViewTask)

    return render(request,'addtask.html')

def ViewTask(request):
    user_id = request.user.id
    data = UserTask.objects.filter(status="pending",user_id=user_id).order_by('due_date')
    return render(request,'viewtask.html',{'data':data})

def TaskStatus(request,id):
    data = UserTask.objects.get(id=id)
    data.status = "completed"
    data.save()
    return redirect(ViewTask)

def DeleteTask(request,id):
    data = UserTask.objects.get(id=id)
    data.delete()
    return redirect(ViewTask)

def CompletedTask(request):
    user_id = request.user.id
    data = UserTask.objects.filter(status="completed",user_id=user_id)
    return render(request,'Completed.html',{'data':data})

def DetailedView(request,id):
    data = UserTask.objects.get(id=id)
    return render(request,'Detailedview.html',{'data':data})

def Edit(request,id):
    data = UserTask.objects.get(id=id)
    return render(request, 'update.html', {'data': data})

def Update(request,id):

    if request.method == 'POST':

        data = UserTask.objects.get(id=id)
        data.task_name = request.POST['task']
        data.due_date = request.POST['due']
        data.status = request.POST['status']
        data.discrp = request.POST['discrp']

        data.save()
        return redirect(ViewTask)
    return render(request,'update.html')

def Forgot_password(request):
    if request.method == 'POST':

        mobile = request.POST['phone']
        userdata = UserProfile.objects.get(phone=mobile)   # registered mobile number of user
        if userdata:
            url = "http://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/{}/AUTOGEN".format(str(mobile))

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=payload, headers=headers)
            data = response.json()

            r = data['Details']
            request.session['Details'] = r
            request.session['phone'] = mobile
            if data['Status'] == 'Success':
                return redirect(reset_password)
        else:
            return redirect(Forgot_password)
    return render(request, 'forgot.html')

def reset_password(request):
    if request.method == 'POST':
        otp = request.POST['OTP']
        passwd = request.POST['passw']
        cpasswd = request.POST['cpassw']
        details = request.session.get('Details')
        api = 'https://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/VERIFY/{}/{}'.format(details, otp)
        res = requests.get(api).json()
        print(res)
        phone = request.session.get('phone')
        if res['Status'] == 'Success':
            if passwd == cpasswd:
                userdata = UserProfile.objects.get(phone=phone)
                data = User.objects.get(id=userdata.user_id)
                u = User.objects.get(username = data.username)
                u.set_password(passwd)
                u.save()

                return redirect(user_login)
    return render(request,'verify.html')

def Dashboard(request):
    return render(request,'dashbord.html')

def CreateProfile(request):
    data = User.objects.get(id=request.user.id)
    if request.method == "POST":
        phone = request.POST['phone']
        dob = request.POST['DOB']
        address = request.POST['addr']
        city = request.POST['city']

        prof = UserProfile.objects.create(user_id=request.user.id, phone=phone, DOB=dob, address=address, city=city)
        prof.save()
        return redirect(ViewProfile)
    return render(request,'profile.html',{"data": data})


def ViewProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = UserProfile.objects.get(user_id=current_user.id)
    date_join = data.date_joined
    return render(request,'viewprofile.html',{'data': data, "data1": data1, 'date_join': date_join.date()})

def EditProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['DOB']
        address = request.POST['addr']
        city = request.POST['city']

        User.objects.filter(id=current_user.id).update(first_name=first_name,last_name=last_name,email=email)
        UserProfile.objects.filter(user_id = current_user.id).update(phone=phone,DOB=dob,address=address,city=city)
        return redirect(ViewProfile)
    return render(request, 'editpro.html', {'data': data,'data1':data1})

def Change_password(request):

    if request.method == 'POST':
        old_pass = request.POST['old']
        new_pass = request.POST['new']
        cnf_pass = request.POST['cnew']
        data = check_password(old_pass, request.user.password)
        if data:
            if new_pass == cnf_pass:
                u = User.objects.get(username=request.user.username)
                u.set_password(new_pass)
                u.save()
                print("password change successfully")

            else:
                print('password is not matching')
                return redirect(Change_password)
        else:
            print('Enter the correct password')
            return redirect(Change_password)

    return render(request, 'changepass.html')


