from django.shortcuts import render

def draw_banner(request):
	text = request.GET['text']
	context = {
		'bannerContent': text, 
	}
	return render( request, "visitorapp/banner.svg", context, content_type='image/svg+xml' )

def draw_ring(request):
	text = request.GET['text']
	context = {
		'bannerContent': text, 
	}
	return render( request, "visitorapp/ring.svg", context, content_type='image/svg+xml' )
