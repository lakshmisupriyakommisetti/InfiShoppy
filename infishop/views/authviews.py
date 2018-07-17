from django.views import View
from django.shortcuts import render,get_object_or_404,redirect
from infishop.forms.auth import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout,authenticate


class SignupView(View):
    def get(self,request,*args,**kwargs):
        form = SignupForm
        return render( request,template_name='signup.html',context={'form':form})

    def post(self,request):
        form = SignupForm(request.POST)
        if(form.is_valid()):
            user = User.objects.create_user(**form.cleaned_data)
            my_group = Group.objects.get(name='infiusers')
            my_group.user_set.add(user)
            user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request,user)
                return redirect('infishop:categoryList')
        else:
            return redirect('infishop:signup')



class LoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm
        return render( request,template_name='login.html',context={'form':form})
    def post(self,request):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('infishop:categoryList')
        return redirect('infishop:login')

def Logout_user(request):
    logout(request)
    return redirect('infishop:home')

