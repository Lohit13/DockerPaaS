from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import logout as auth_logout
from django.contrib import auth

def index(request):
	if request.user.is_authenticated():
		x = request.user.email
		if x[len(x)-11:] != 'iiitd.ac.in':
			logout(request)
		return HttpResponseRedirect("/home")

	return render_to_response('index.html')


def logout(request):
	auth_logout(request)
	args = {}
	args.update(csrf(request))
	
	return HttpResponseRedirect("/")
