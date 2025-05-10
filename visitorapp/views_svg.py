from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

import math ;

from .vec import VecSpace

def draw_banner(request):
	text = request.GET['text']
	context = {
		'bannerContent': text, 
	}
	return render( request, "visitorapp/banner.svg", context, content_type='image/svg+xml' )
