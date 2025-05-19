from django.shortcuts import render

import re

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
	return render_svg( request, "visitorapp/banner.svg", context )


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
	return render_svg( request, "visitorapp/ring.svg", context )

# Chrome:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
# Safari:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15
# Firefox: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0

RE_CHROM_USER_AGENT = re.compile( r'(^|\s)Chrome/[.\d]+(\s|$)' )

def render_svg( request, resource, context ):
	if "HTTP_USER_AGENT" in request.META:
		userAgent = request.META["HTTP_USER_AGENT"]
		if RE_CHROM_USER_AGENT.search( userAgent ):
			chromeResource = resource.replace( '.svg', '.chrome.svg' )
			print( f'detected Chrome; rendering {chromeResource} instead of {resource}' )
			resource = chromeResource
	return render( request, resource, context, content_type='image/svg+xml' )
