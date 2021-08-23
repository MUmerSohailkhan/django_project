from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .form import userregisterform,userupdateform,Profileupdateform
from django.contrib.auth.decorators import login_required
# Create your views here.


def registration(request):
    if request.method =='POST':
        form=userregisterform(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username} know you can login!')
            return redirect('login')
    else:
        form=userregisterform()

    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        u_form=userupdateform(request.POST, instance=request.user)
        p_form=Profileupdateform(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account has been updated!')
            return redirect('profile')

    else:
        u_form = userupdateform(instance=request.user)
        p_form = Profileupdateform(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form


    }

    return render(request,'users/profile.html',context)