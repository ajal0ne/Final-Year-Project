from django.shortcuts import render,redirect
from .models import *
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def index(request):
    return render(request, 'job/index.html')

def admin_login(request):
    error =""
    if request.method=='POST':
        u=request.POST['u_name']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'job/admin_login.html',d)

def user_login(request):
    error=""
    if request.method =='POST':
        u=request.POST['u_name']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1= StudentUser.objects.get(user=user)
                if user1.type=="student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request, 'job/user_login.html',d)

def recruiter_login(request):
    error=""
    if request.method =='POST':
        u=request.POST['u_name']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1= Recruiter.objects.get(user=user)
                if user1.type=="recruiter" and user1.status!="pending":
                    login(request,user)
                    error="no"
                else:
                    error="not"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request, 'job/recruiter_login.html',d)
    

def recruiter_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['f_name']
        l=request.POST['l_name']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        company=request.POST['company']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e ,password=p)
            Recruiter.objects.create(user=user,mobile=con,gender=gen,company=company,type="recruiter",status="pending")
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'job/recruiter_signup.html',d)


def user_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['f_name']
        l=request.POST['l_name']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e ,password=p)
            StudentUser.objects.create(user=user,mobile=con,gender=gen,type="student")
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'job/user_signup.html',d)
    
def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['f_name']
        l=request.POST['l_name']
        con=request.POST['contact']
        gen=request.POST['gender']

        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
    d={'student':student,'error':error}
    return render(request, 'job/user_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'job/admin_home.html')

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['f_name']
        l=request.POST['l_name']
        con=request.POST['contact']
        gen=request.POST['gender']

        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con
        recruiter.gender=gen
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request, 'job/recruiter_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index_page')


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'job/view_user.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request,'job/recruiter_pending.html',d)

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
    d={'recruiter':recruiter, 'error':error}
    return render(request,'job/change_status.html',d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accept')
    d={'data':data}
    return render(request,'job/recruiter_accepted.html',d)



def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Reject')
    d={'data':data}
    return render(request,'job/recruiter_rejected.html',d)


def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'job/recruiter_all.html',d)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'job/change_passwordadmin.html',d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'job/change_passworduser.html',d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        o=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'job/change_passwordrecruiter.html',d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=='POST':
        j=request.POST['jobtitle']
        sd=request.POST['startdate']
        ld=request.POST['enddate']
        s=request.POST['salary']
        loc=request.POST['location']
        exp=request.POST['experience']
        sk=request.POST['skills']
        des=request.POST['description']
        user=request.user
        recruiter=Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ld,title=j,salary=s,description=des,experience=exp,skills=sk,location=loc)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'job/add_job.html',d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'job/job_list.html',d)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        j=request.POST['jobtitle']
        sd=request.POST['startdate']
        ld=request.POST['enddate']
        s=request.POST['salary']
        loc=request.POST['location']
        exp=request.POST['experience']
        sk=request.POST['skills']
        des=request.POST['description']
        job.title=j
        job.salary=s
        job.experience=exp
        job.location=loc
        job.skills=sk
        job.description=des
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        else:
            pass
        if ld:
            try:
                job.end_date=ld
                job.save()
            except:
                pass
        else:
            pass
    d={'error':error, 'job':job}
    return render(request, 'job/edit_jobdetail.html',d)

def latest_jobs(request):
    data=Job.objects.all().order_by('-start_date')
    d={'data':data}
    return render(request,'job/latest_jobs.html',d)


def user_latestjobs(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li':li}
    return render(request,'job/user_latestjobs.html',d)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request,'job/job_detail.html',d)


def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=datetime.date.today()
    if job.end_date<date1:
        error="close"
    elif job.start_date>date1:
        error="notopen"
    else:
        if request.method=='POST':
            r=request.FILES['resume']
            Apply.objects.create(job=job,student=student, resume=r,applydate=datetime.date.today())
            error="done"
    d={'error':error}
    return render(request,'job/applyforjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=Apply.objects.all()
    d={'data':data}
    return render(request,'job/applied_candidatelist.html',d)







