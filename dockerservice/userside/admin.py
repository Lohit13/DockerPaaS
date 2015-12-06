from django.contrib import admin
from .models import *

# Register your models here.

Models = [VM,Docker]

admin.site.register(Models)







