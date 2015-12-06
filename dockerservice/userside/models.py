from django.db import models
from django.contrib.auth.models import User
import json

class VM(models.Model):
	name = models.CharField(max_length=100)
	user = models.CharField(max_length=100)
	ip = models.CharField(max_length=15)
	password = models.TextField()
	ram = models.IntegerField(default=2)

	def __unicode__(self):
		return self.name

class Docker(models.Model):
	name = models.CharField(max_length=100)
	password = models.TextField()
	vm = models.ForeignKey(VM)
	ports = models.TextField()
	user = models.ForeignKey(User)

	def setport(self, x):
		self.ports = json.dumps(x)

	def getport(self, x):
		return json.loads(self.ports)
	
	def __unicode__(self):
		return self.name