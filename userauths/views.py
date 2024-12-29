from django.shortcuts import render,redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register_view(request):
  if request.user.is_authenticated:
    messages.warning(request,f"You are already logged in.")
    return redirect("rest:home")

  if request.method=="POST":
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
      new_user=form.save()
      username=form.cleaned_data.get("username")
      messages.success(request,f"Hey {username}, welcome to a place where good food matters!")
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
      return render(request, "userauths/sign-in.html", {})

    user=authenticate(request,email=email, password=password)

    if user is not None:
      login(request,user)
      messages.success(request,"You are Logged In.")
      next_url = request.GET.get('next', 'rest:home')
      return redirect(next_url)
    
    else:
      messages.warning(request,"Wrong password entered.")
  
  context={}
  return render(request,"userauths/sign-in.html",context)


def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    
    return redirect("userauths:sign-in")


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('userauths:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'userauths/profile.html', context)
