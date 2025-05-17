from django.http import QueryDict
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from django.db.models import Q

from datetime import datetime, timedelta
import colorsys

from .models import Wall, Visitor, Inscription

def about(request):
	context = {	}
	return render( request, "visitorapp/about.html", context )

def index(request):
	context = {
		'wall_list': Wall.objects.order_by('-created_date'),
	}
	return render( request, "visitorapp/index.html", context )

BADGE_KEYS = [ 'flower-001', 'bicycle-001', 'heart-001', 'cake-001' ,'tea-001','cactus-001','cherry-blossom-001']
BADGE_IMAGES = {
	'flower-001': 'visitorapp/2693808_abstract ecology_abstraction_environmental_flower_leaves_icon.svg',
	'heart-001': 'visitorapp/9004758_heart_love_valentine_like_icon.svg',
	'bicycle-001': 'visitorapp/3850763_activity_bicycle_cycling_riding_sport_icon.svg',
	'cake-001': 'visitorapp/6334501_cake_dessert_love_party_sweet_icon.svg',
	'tea-001' : 'tea-001',
	'cherry-blossom-001' : 'cherry-blossom-001',
	'cactus-001' : 'cactus-001',
	
}

def show_wall(request, wall_id ):
	tutorialOverride = 'tutorial' in request.GET

	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	datetime_cutoff = datetime.now() - timedelta(hours=1, minutes=0)
	query = (
		Q(moderation_status='ok') | # show because it's been reviewed and is ok
		(
			Q(visitor_id=visitor.id) & # show because this visitor wrote it ...
			~Q(moderation_status='removed') # ... and it hasn't been removed
		) |
		(
			Q(moderation_status='new') & # show because it hasn't been moderated ...
			Q(created_date__gte=datetime_cutoff)  # ... but it was just created recently
		)
	)
	inscriptions = wall.inscription_set.filter(query).order_by('-id');

	editInscription = int(request.GET['editInscription']) if 'editInscription' in request.GET else None

	badgeList = [ make_badge(i,visitor, editInscription == i.id ) for i in inscriptions ]
	editBadge = next( (b for b in badgeList if b['id'] == editInscription), None )

	myBadgeList = [ b for b in badgeList if b['is_mine'] ]
	tutorial = tutorialOverride or len(myBadgeList) == 0

	context = {
		'wall': wall,
		'edit_inscription': editInscription,
		'badge_list': badgeList,
		'edit_badge': editBadge,
		'tutorial': tutorial,
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
	editorLocation = 'upper' if position['y'] > 50 else 'lower'
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
	return f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'

def image_from_int( n ):
	i = n % len(BADGE_KEYS)
	k = BADGE_KEYS[ i ]
	return BADGE_IMAGES[ k ]

INITIAL_TEXT = 'inscribe your message here'

def add_inscription(request, wall_id):
	wall = get_object_or_404( Wall, pk=wall_id )
	visitor = current_visitor( request )
	inscription = Inscription.objects.create(
		wall=wall,
		visitor=visitor,
		text=INITIAL_TEXT,
		moderation_status='new',
		created_date=datetime.now()
		)
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
