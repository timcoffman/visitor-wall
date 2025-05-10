from django.http import HttpResponse

from drawsvg import Drawing, Path, Use

import math ;
import pprint ;

from .vec import VecSpace

def draw_banner(request):
	text = request.GET['text']
	widthToHeight = len(text) / 3.0
	
	arc = math.pi / 2.0
	inner = 0.9
	baseline = 0.92
	outer = 1.0
	a1 = -arc/2.0
	a2 = arc/2.0
	s = VecSpace()
	c1 = s.vec2(inner,0).rotate(a1)
	c1k = s.vec2(inner,0.2).rotate(a1)
	c2k = s.vec2(outer,-0.2).rotate(a1)
	c2 = s.vec2(outer,0).rotate(a1)
	c3 = s.vec2(outer,0).rotate(a2)
	c3k = s.vec2(outer,0.2).rotate(a2)
	c4k = s.vec2(inner,-0.02).rotate(a2)
	c4 = s.vec2(inner,0).rotate(a2)
	b1 = s.vec2(baseline,0).rotate(a2)
	b1k = s.vec2(baseline,0.2).rotate(a2)
	b2k = s.vec2(baseline,-0.2).rotate(a2)
	b2 = s.vec2(baseline,0).rotate(a1)
	s.fit( widthToHeight, 1.0 )
	
	svgPathForText = Path().M(*b1).C(*b1k, *b2k, *b2)
	print( f'svgPathForText = {pprint.pp(svgPathForText)}' )
	svgPathForBanner = Path() \
		.M(*c1) \
		.C(*c1k, *c2k, *c2) \
		.L(*c3) \
		.C(*c3k, *c4k, *c4) \
		.Z()

	s2 = VecSpace()
	p = s2.vec2(0.0,0.0)
	q = s2.vec2(0.0,1.0)
	j = s2.vec2(1.0,1.0)
	k = s2.vec2(1.0,0.0)
	s2.rotate(math.pi/6.0)
	s2.fit( widthToHeight, 1.0 )

	drawing = Drawing( widthToHeight, 1)
	drawing.set_render_size(100 * widthToHeight, 100)
	# drawing.append( Description( f'banner containing the text "{bannerContent}"' ) )
	svgPathForTest = Path().M( p.x, p.y ).L( q.x, q.y ).L( j.x, j.y ).L( k.x, k.y ).Z()
	drawing.append( Use(svgPathForTest, 0, 0, fill="none", stroke="red", stroke_width="0.05") )
	drawing.append( Use(svgPathForBanner, 0, 0, fill="none", stroke="green", stroke_width="0.05") )
	drawing.append( Use(svgPathForText, 0, 0, fill="none", stroke="blue", stroke_width="0.05") )
	return HttpResponse( drawing.as_svg(), content_type='image/svg+xml' );
