from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import re

def index(request):
	return render(request, 'accounts/index.html')

def process(request):
	if request.method == 'POST':

		# LOGIN
		if 'login' in request.POST:
			# validations:
			login_errors = []
			if not request.POST['username']:
				login_errors.append('Username is required')
			if not request.POST['password']:
				login_errors.append('Password is required')
			if login_errors:
				for i in login_errors:
					messages.error(request, i, extra_tags="login_error")
				return redirect('/')
			else:
				query_check = User.objects.get(username=request.POST['username'])
				if not query_check:
					login_errors.append('User does not exist')
				if not check_password(request.POST['password'], query_check.password):
					login_errors.append('Incorrect password')
				if login_errors:
					for i in login_errors:
						messages.error(request, i, extra_tags="login_error")
					return redirect('/')
				else:
					request.session['id'] = query_check.id
					return redirect('/home')

		# REGISTER
		if 'register' in request.POST:
			# validations:
			EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
			noNumbers = re.compile(r'^[^0-9]+$')
			registration_errors = []
			if not request.POST['username']:
				registration_errors.append('Username is required')
			if not request.POST['firstname']:
				registration_errors.append('First Name is required')
			elif not noNumbers.match(request.POST['firstname']):
				registration_errors.append('First name cannot contain numbers')
			if not request.POST['lastname']:
				registration_errors.append('Last Name is required')
			elif not noNumbers.match(request.POST['lastname']):
				registration_errors.append('Last name cannot contain numbers')
			if not request.POST['email']:
				registration_errors.append('Email is required')
			elif not EMAIL_REGEX.match(request.POST['email']):
				registration_errors.append('Invalid email')
			if not request.POST['password1']:
				registration_errors.append('Password is required')
			elif request.POST['password1'] != request.POST['password2']:
				registration_errors.append('Password does not match')
			if registration_errors:
				for i in registration_errors:
					messages.error(request, i, extra_tags="registration_error")
				return redirect('/')
			else:
				query_check = User.objects.filter(username=request.POST['username'])
				if query_check.count() > 0:
					registration_errors.append('Username already taken')
				if registration_errors:
					for i in registration_errors:
						messages.error(request, i, extra_tags="registration_error")
					return redirect('/')
				else:
					hashed_password = make_password(request.POST['password1'])
					new_user = User.objects.create(username=request.POST['username'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password=hashed_password)
					new_user.save()
					request.session['id'] = new_user.id
	                return redirect('/home')
	return redirect('/')

def home(request):
	if request.session['id'] == None:
		return redirect('/')
	users = User.objects.all()
	print users
	context = {
		'users': users
	}
	return render(request, 'accounts/home.html', context)

def logout(request):
	request.session['id'] = None
	return redirect('/')


































