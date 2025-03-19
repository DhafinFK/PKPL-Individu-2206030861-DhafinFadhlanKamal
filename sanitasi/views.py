from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegistrationForm
import json

def register(request):
    if request.POST:
        form = UserRegistrationForm(request.POST or None)  
    else:
        return render(request, "sanitasi/register.html", {"form": UserRegistrationForm()})


    if form:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            user_info = "\n".join([f"{key}: {value}" for key, value in vars(user).items() if not key.startswith('_')])

            return HttpResponse(f"Berhasil Menambahkan User:\n\n{user_info}", content_type="text/plain")
    
    print(form.errors)
    return render(request, "sanitasi/register.html", {"form": form})

