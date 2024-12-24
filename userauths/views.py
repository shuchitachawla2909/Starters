from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings

User=settings.AUTH_USER_MODEL

def register_view(request):
  if request.user.is_authenticated:
    messages.warning(request,f"You are already logged in.")
    redirect(request,"rest:home")

  if request.method=="POST":
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
      new_user=form.save()
      username=form.cleaned_data.get("username")
      messages.success(request,f"Hey {username}, welcome to a place where good food matters!")
      new_user=authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])
      login(request,new_user)
      return redirect("rest:home")

  else:
    form=UserRegisterForm()
    

  
  context={
    'form':form,

  }
  return render(request,"userauths/sign-up.html",context)


def login_view(request):
  if request.user.is_authenticated:
    return redirect("rest:home")
  
  if request.method== "POST":
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
      user=User.objects.get(email=email)
    except:
      messages.warning(request,f"User with email {email} does not exist.")

    user=authenticate(request,email=email, password=password)

    if user is not None:
      login(request,user)
      messages.success(request,"You are Logged In.")
      return redirect("rest:home")
    else:
      messages.warning(request,"Wrong password entered.")
  
  context={}
  return render(request,"userauths/sign-in.html",context)


def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    
    return redirect("userauths:sign-in")



