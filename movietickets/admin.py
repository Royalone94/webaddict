from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields  = ['name', 'description', 'cast', 'trailer', 'director']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	search_fields  = ['no']