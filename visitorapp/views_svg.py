from django.shortcuts import render

def draw_banner(request):
	text = request.GET['text']
	# banner font-size can range between 0.5 and 0.3
	# maximum number of letters at 0.5 is 24
	# optimal number of letters at 0.3 is 36
	fontScale = 1.0 - ( len(text) - 24 ) / (36-24)
	fontSize = fontScale * (0.5 - 0.3) + 0.3
	bannerFontSize = min(0.5,max(0.3, fontSize))

	bannerFill = request.GET['bg'] if 'bg' in request.GET else 'white'

	context = {
		'bannerContent': text,
		'bannerFontSize': f'{bannerFontSize:.2f}',
		'bannerFill': bannerFill,
	}
	return render( request, "visitorapp/banner.svg", context, content_type='image/svg+xml' )

def draw_ring(request):
	text = request.GET['text']
	# banner font-size can range between 0.2 and 0.1
	# maximum number of letters at 0.2 is 24
	# optimal number of letters at 0.1 is 48
	fontScale = 1.0 - ( len(text) - 24 ) / (48-24)
	fontSize = fontScale * (0.2 - 0.1) + 0.1
	bannerFontSize = min(0.2,max(0.1, fontSize))

	bannerFill = request.GET['bg'] if 'bg' in request.GET else 'white'

	context = {
		'bannerContent': text,
		'bannerFontSize': f'{bannerFontSize:.2f}',
		'bannerFill': bannerFill,
	}
	return render( request, "visitorapp/ring.svg", context, content_type='image/svg+xml' )
