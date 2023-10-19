from django.contrib import admin

# Register your models here.
from app.models import NewUser,TodoModel

admin.site.register(NewUser)
admin.site.register(TodoModel)