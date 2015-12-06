from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import logout as auth_logout
from django.contrib import auth
from passlib.hash import sha512_crypt
from django.core.files import locks
from django.core.files.move import file_move_safe
import os
import threading
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import EmailMultiAlternatives
	
def write_variable_file_1(user, password):
	hashed_password = sha512_crypt.encrypt(password)

	towrite = '---' +'\n'
	towrite += '\n'
	towrite += ('user: "' + user + '"\n')
	towrite += ('password: "' + hashed_password +'"\n')
	towrite += '\n'
	towrite += ('dockercmd: "docker run -d --name ' + user + ' -it ubuntu"' +'\n')
	towrite += '\n'
	towrite += ('linetoadd1: "me=`whoami`"' + '\n')
	towrite += ('linetoadd2: "if [ $me == \'' + user + '\' ]; then"' + '\n')
	towrite += ('linetoadd3: "  docker exec -it ' + user + ' /bin/bash\\nfi"' + '\n')

	with open('test.yml', 'wb') as f:
		locks.lock(f, locks.LOCK_EX)
		f.write(towrite)

	file_move_safe("test.yml", "../Ansible/variables.yml", allow_overwrite = True)

def write_variable_file_2(user):

	towrite = '---' +'\n'
	towrite += '\n'
	towrite += ('user: "' + user + '"\n')

	with open('test2.yml', 'wb') as f:
		locks.lock(f, locks.LOCK_EX)
		f.write(towrite)

	file_move_safe("test2.yml", "../Ansible/variables2.yml", allow_overwrite = True)

def write_hosts_file(vm,password):

	towrite = '[vm]' + '\n'
	towrite += str(vm) + " ansible_ssh_pass='" + str(password) + "'"

	with open('hosts', 'wb') as f:
		locks.lock(f, locks.LOCK_EX)
		f.write(towrite)

	file_move_safe("hosts", "../Ansible/hosts", allow_overwrite = True)


def createdocker(user, instance, vm, email):
	try:
		with open(user, 'wb') as f:
			locks.lock(f, locks.LOCK_EX)
			f.write('0')
		os.system('ansible-playbook ../Ansible/newdock.yml -i ../Ansible/hosts')
		with open(user, 'wb') as f:
			locks.lock(f, locks.LOCK_EX)
			f.write('1')
		body = 'New Docker Instance Created\n'
		body += 'IP : ' + str(instance.vm.ip) + '\n'
		body += 'User : ' + str(instance.name) + '\n'
		body += 'Password : ' + str(instance.password) + '\n'
		msg = EmailMultiAlternatives(subject="DockerPaaS | New Instance Created", body=body,from_email="admin@dockerpaas.com",to=[email])
		msg.send()
	except:
		print 'no'

	instance.save()
	vm.save()

@login_required(login_url='/',redirect_field_name=None)
def home(request):
	if request.method == "POST":
		args = {}
		args.update(csrf(request))

		#PUT CHECK IF NAME IS ALREADY TAKEN!!!			
		try:
			d = Docker.objects.get(name=request.POST["name"])
			args['msg'] = 'Name already taken. Try something else!'
			return render_to_response('home.html', args)
		except:
			pass

		#Check if vm space is still available
		try:
			vm = VM.objects.filter(ram__gte=1)[0]
		except:
			args['msg'] = 'Sorry, no VMs currently available'
			return render_to_response('home.html', args)

		# write hosts file
		write_hosts_file(vm.ip,vm.password)

		# write variables1.yml
		write_variable_file_1(request.POST["name"], request.POST["pass"])


		instance = Docker(name=request.POST["name"],vm=vm,password=request.POST["pass"],user=request.user)
		vm.ram = vm.ram-1


		t1 = threading.Thread(target=createdocker,args=(request.POST["name"], instance, vm, request.user.email))
		t1.start()

		args['requested'] = True
		args['reqname'] = request.POST["name"]
		# args['msg'] = 'Instance Created!'
		args['msg'] = "Creating instance, please wait"

		return render_to_response('home.html', args)
	else:
		args = {}
		args.update(csrf(request))

		return render_to_response('home.html', args)

@login_required(login_url='/',redirect_field_name=None)
def manage(request):
	instances = Docker.objects.filter(user=request.user)

	args = {}
	args['instances'] = instances

	return render_to_response('manage.html', args)

def destroy_instance(name):
	try:
		write_variable_file_2(name)
		os.system('ansible-playbook ../Ansible/desdock.yml -i ../Ansible/hosts')
	except:
		print 'no'

@login_required(login_url='/',redirect_field_name=None)
def destroy(request,name=''):
	try:
		instance = Docker.objects.get(name=name)

		if(instance.user != request.user):
			return HttpResponseRedirect('/')

		t1 = threading.Thread(target=destroy_instance,args=(name,))
		t1.start()

		vm = instance.vm
		instance.delete()
		vm.ram = vm.ram + 1
		vm.save()

		print ':)'
		os.remove(name)
		return HttpResponseRedirect('/dashboard/')

	except:
		print ':('
		return HttpResponseRedirect('/dashboard/')

@login_required(login_url='/',redirect_field_name=None)
def checkStatus(request, user = ''):
	val = ""
	with open(user, 'rb') as f:
		locks.lock(f, locks.LOCK_EX)
		val = f.read()

	return HttpResponse(val)
