from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Wall, Visitor, Inscription

def index(request):
	context = {
		'wall_list': Wall.objects.order_by('-created_date'), 
	}
	return render( request, "visitorapp/index.html", context )

def show_wall(request, wall_id ):
	context = {
		'wall': get_object_or_404( Wall, pk=wall_id ),
	}
	return render( request, "visitorapp/wall.html", context )

def add_inscription(request, wall_id):
	wall = get_object_or_40