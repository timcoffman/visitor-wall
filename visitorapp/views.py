from django.http import QueryDict
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse

import colorsys

from .models import Wall, Visitor, Inscription

def index(request):
	context = {
		'wall_list': Wall.objects.order_by('-created_date'),
	}
	return render( request, "visitorapp/index.html", context )

BADGE_KEYS = [ 'flower-001', 'bicycle-001', 'heart-001', 'cake-001' ]
BADGE_IMAGES = {
	'flower-001': 'visitorapp/2693808_abstract ecology_abstraction_environmental_flower_leaves_icon.svg',
	'heart-001': 'visitorapp/9004758_heart_love_valentine_like_icon.svg',
	'bicycle-001': 'visitorapp/3850763_activity_bicycle_cycling_riding_sport_icon.svg',
	'cake-001': 'visitorapp/6334501_cake_dessert_love_party_sweet_icon.svg',
}

def show_wall(request, wall_id ):
	wall = get_object_or_404( Wall, pk=wall_id )
	inscriptions = wall.inscription_set.order_by('-id');
	visitor = current_visitor( request )
	editInscription = int(request.GET['editInscription']) if 'editInscription' in request.GET else None
	badgeList = [ make_badge(i,visitor, editInscription == i.id ) for i in inscriptions ]
	editBadge = next( (b for b in badgeList if b['id'] == editInscription), None )
	context = {
		'wall': wall,
		'edit_inscription': editInscription,
		'badge_list': badgeList,
		'edit_badge': editBadge,
	}
	return render( request, "visitorapp/wall.html", context )

def current_visitor( request ):
	if request.session.session_key is None:
		request.session.save()
	visitor, visitor_created = Visitor.objects.get_or_create( cookie=request.session.session_key, defaults={} )
	return visitor

def make_badge( inscription, currentVisitor, isSelected ):
	position = position_from_int( inscription.id )
	bg = bg_from_int( inscription.id )
	skew = skew_from_int( inscription.id )
	editorLocation = 'upper' if position['y'] > 5 else 'lower'
	staticImage = image_from_int( inscription.id )
	badge = {
		'id': inscription.id,
		'text': inscription.text,
		'static_image': staticImage,
		'is_mine': currentVisitor.id == inscription.visitor_id,
		'is_selected': isSelected,
		'position': position,
		'skew': skew,
		'bg': bg,
		'editor_location': editorLocation,
		}
	return badge

POS_M = 27644437
POS_D = 1932.0

def position_from_int( n ):
	q = ( n * POS_M ) % (POS_D*POS_D)
	x = (q // POS_D) / POS_D
	y = (q % POS_D) / POS_D
	return { 'x': int(x * 100), 'y': int(y * 100) }

def skew_from_int( n ):
	q = ( n * POS_M ) % (POS_D)
	k = q / POS_D * 10.0 - 5.0
	return k

def bg_from_int( n ):
	q = ( n * POS_M ) % (POS_D)
	h = q / POS_D * 1.00
	rgb = colorsys.hsv_to_rgb( h, 0.07, 1.0 )
	print( f'h -> rgb = {0.77 + h} -> {rgb}')
	return f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'

def image_from_int( n ):
	i = n % len(BADGE_KEYS)
	k = BADGE_KEYS[ i ]
	return BADGE_IMAGES[ k ]

def add_inscription(request, wall_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	inscription = Inscription.objects.create( wall=wall, visitor=visitor, text='inscribe your message here' )
	q = QueryDict(mutable=True)
	q['editInscription'] = inscription.id
	return redirect( reverse( 'show_wall', args=(wall.id,), query=q ) )

def update_inscription(request, wall_id, inscription_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	if 'commit' in request.POST:
		visitor = current_visitor( request )
		inscription = get_object_or_404( Inscription, pk=inscription_id )
		if ( visitor.id != inscription.visitor_id ):
			return HttpResponse( f'not authorized to rewrite this inscription', status=401)
		inscription.text = request.POST['text']
		inscription.save()
	return redirect( reverse( 'show_wall', args=(wall.id,) ) )
