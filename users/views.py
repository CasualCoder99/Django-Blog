from django.shortcuts import render,redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from blog.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

def unathenticated_user(view_func):

    def wrapper_func(request,*args,**kwargs):
        if(request.user.is_authenticated):
            return redirect('post_list')
        else:
        	return view_func(request,*args,**kwargs)

    return wrapper_func

@unathenticated_user
def register(request):
	if(request.method=='POST'):
		form=UserRegisterForm(request.POST)
		if(form.is_valid()):
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,f'Congrats! Account created. You can now Log In')
			return redirect('/login')

	form=UserRegisterForm()
	return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
	posts=Post.objects.filter(author=request.user).order_by('-published_date')
	context={'posts':posts,'user':request.user,'profile':request.user.profile}
	return render(request,'users/profile.html',context)

@login_required	
def edit_profile(request):
	
	if(request.method=='POST'):
		u_form=UserUpdateForm(request.POST,instance=request.user)
		p_form=ProfileUpdateForm(request.POST,instance=request.user.profile)
		print('POST!!!!')
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.success(request,f'Changes have been saved')
			return redirect('/profile')
	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	
	context={'u_form':u_form,'p_form':p_form}
	return render(request,'users/edit_profile.html',context)