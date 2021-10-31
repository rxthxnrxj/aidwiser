from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Aid)
admin.site.register(Ambulance)
admin.site.register(Hospital)
admin.site.register(Doctor)
