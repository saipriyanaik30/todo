from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method=='POST':
        username=request.POST.get('fnm')
        email=request.POST.get('emailid')
        password=request.POST.get('pwd')
        my_user=User.objects.create_user(username,email,password)
        my_user.save()
        return redirect('/loginn')
    
    return render(request,'signup.html')

def loginn(request):
    if request.method=='POST':
        usern=request.POST.get('fnm')
        passw=request.POST.get('pwd')
        #print(usern,passw)
        userr=authenticate(request,username=usern,password=passw)
        if userr is not None:
            login(request,userr)
            return redirect('/todopage')
        else :
            return redirect('/loginn')
    return render(request,'loginn.html')    

@login_required(login_url='/loginn')
def todopage(request):
    if request.method=='POST':
        title1=request.POST.get('title')
        print(title1)
        obj=models.TODO(title=title1,user=request.user)
        obj.save()
        user=request.user
        res=models.TODO.objects.filter(user=user).order_by('-date')
        return redirect('/todopage',{'res' : res})
    res=models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request,'todopage.html',{'res':res})


def signoutt(request):
    logout(request)  
    return redirect('/loginn')

@login_required(login_url='/loginn')
def edit_todo(request,srno):
    if request.method=='POST':
        title1=request.POST.get('title')
        print(title1)
        obj=models.TODO.objects.get(srno=srno)
        obj.title=title1
        obj.save()
        user=request.user
        return redirect('/todopage',{'obj':obj})
    
    obj=models.TODO.objects.get(srno=srno)
    return render(request,'todopage.html')    

@login_required(login_url='/loginn')
def delete_todo(request,srno):
    obj=models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

  


