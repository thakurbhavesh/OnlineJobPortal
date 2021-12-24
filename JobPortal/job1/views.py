from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import datetime, date
import time


y=time.strftime('%H:%M:%S')
x=datetime.now
# Create your views here.
def home(request):


    return render(request,'home.html',{'date':x})



def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":
        f = request.POST['jobtitle']
        l = request.POST['startdate']
        i = request.POST['enddate']
        p = request.POST['salary']
        e = request.FILES['logo']
        cn = request.POST['experience']
        lo = request.POST['location']
        sk = request.POST['skills']
        des = request.POST['description']


        try:
            Job.objects.create(start_date=l,end_date=i,salary=p,logo=e,experience=cn,location=lo,skills=sk,description=des,title=f,creationdate=date.today())
            error = "no"

        except:
            error = "yes"
    d = {'error': error}


    return render(request,'add_job.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == "POST":
        f = request.POST['jobtitle']
        l = request.POST['startdate']
        i = request.POST['enddate']
        p = request.POST['salary']

        cn = request.POST['experience']
        lo = request.POST['location']
        sk = request.POST['skills']
        des = request.POST['description']

        job.title=f
        job.salary=p
        job.experience=cn
        job.location=lo
        job.skills=sk
        job.description=des
        try:
            Job.save()
            error = "no"

        except:
            error = "yes"

        if l:
            try:
                job.start_date=l
                job.save()

            except:
                pass

        else:
            pass

        if i:
            try:
                job.end_date = i
                job.save()

            except:
                pass

        else:
            pass

    d = {'error': error,'job':job}
    return render(request,'edit_jobdetail.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    job= Job.objects.all()
    d = {'job': job}
    return render(request, 'job_list.html', d)

def latestjob_list(request):

    job= Job.objects.all().order_by('-start_date')
    d = {'job': job}
    return render(request, 'latestjob_list.html', d)

def admin_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"

            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student= StudentUser.objects.get(user=user)
    d = {'student': student}
    return render(request,'user_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html',{'date':x})

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    d={'recruiter':recruiter}
    return render(request,'recruiter_home.html',d)

def Logout(request):
    logout(request);
    return render(request,'home.html')


def user_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['uname'];
        p = request.POST['pwd'];
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type=="student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"

        else:
            error="yes"
    d={"error":error}
    return render(request,'user_login.html',d)

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"

        else:
            error = "yes"
    d = {"error": error}
    return render(request,'recruiter_login.html',d)


def user_signup(request):
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l =request.POST['lname']
        i= request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        cn = request.POST['contact']
        gen = request.POST['gender']

        try:
           user= User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=cn,image=i,gender=gen,type="student")
           error="no"

        except:
            error="yes"
    d={'error':error}


    return render(request,'user_signup.html',d)

def recruiter_signup(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        cn = request.POST['contact']
        gen = request.POST['gender']
        company= request.POST['company']

        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=cn, image=i, gender=gen, company=company ,type="recruiter",status="pending")
            error = "no"

        except:
            error = "yes"
    d = {'error': error}

    return render(request,'recruiter_signup.html',{'date':x})


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):

    student=StudentUser.objects.get(id=pid)
    student.delete()
    return render(request,'view_users')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status="pending")
    d={'data':data}
    return render(request,'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""

    if request.method=="POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error = "yes"

    d={'error':error}

    return render(request,'change_passwordadmin.html',d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""

    if request.method=="POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error = "yes"

    d={'error':error}

    return render(request,'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""

    if request.method=="POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error = "yes"

    d={'error':error}

    return render(request,'change_passwordrecruiter.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status="Accept")
    d={'data':data}
    return render(request,'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status="Reject")
    d={'data':data}
    return render(request,'recruiter_rejected.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'recruiter_all.html',d)