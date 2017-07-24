from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'loginRegistration_app/index.html')

def success(request):
	return render(request, 'loginRegistration_app/success.html')

def register(request):
	errors = User.objects.validate_registration(request.POST)
	if errors:
		for tag, error in errors.iteritems():
		    messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		found_users = User.objects.filter(email=request.POST['email'])
        if found_users.count() > 0:
            messages.error(request, "email already taken", extra_tags="email")
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            created_user = User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hashed_pw)
            request.session['user_id'] = created_user.id
            request.session['user_name'] = created_user.name
            messages.success(request, 'Thank You for Registering, you may now log in.')
            # print created_user
            # prints to terminal ^
            return redirect('/success')
        return redirect('/')

def login(request):
    found_users = User.objects.filter(email=request.POST['email'])
    if found_users.count() > 0:
        found_users = found_users.first()
        if bcrypt.checkpw(request.POST['password'].encode(), found_users.password.encode()) == True:
            request.session['user_id'] = found_users.id
            request.session['user_name'] = found_users.name
            # print found_users
            return redirect('/success')
        else:
            messages.error(request, "Login Failed", extra_tags="email")
            return redirect('/')
    else:
        messages.error(request, "Login Failed", extra_tags="email")
        return redirect('/')



